# -*- coding: utf-8 -*-
"""Extract edges of polygon layer given a width.

************************************************************************
    Name                : extractedges_algorithm.py
    Date                : May 2025
    Copyright           : (C) 2023-2025 by Laboratorio de Geociencias - FIE
    Email               : geociencias@fie.undef.edu.ar
************************************************************************
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
************************************************************************
"""

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsFeatureSink,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingLayerPostProcessorInterface,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer
)
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QSettings
)
from qgis.PyQt.QtGui import QTransform

import processing


class ExtractEdges(QgsProcessingAlgorithm):
    """Extract edges algorithm class."""

    INPUT = 'INPUT'
    WIDTH = 'WIDTH'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('ExtractEdges', string)

    def rw_settings(self, mode, setting_name, value):
        """Read and write tactilemaps settings.

        If 'mode' is 'r', read the value of 'setting_name',
            or a default 'value'.
        If 'mode' is 'w', write the 'value' in the 'setting_name'.
        """
        directory = ['tactilemaps', self.name(), setting_name]
        setting_path = '/'.join(directory)
        if mode == 'w':
            return QSettings().setValue(setting_path, value)
        elif mode == 'r':
            return QSettings().value(setting_path, value)
        else:
            raise ValueError("Invalid mode. Expected one of 'w' or 'r'.")

    def createInstance(self):
        """Return a new instance of the algorithm."""
        return ExtractEdges()

    def name(self):
        """Return the algorithm name."""
        return 'extractedges'

    def displayName(self):
        """Return the algorithm display name."""
        return self.tr('Extract polygon edges')

    def group(self):
        """Return the name of the group this algorithm belongs to."""
        return ''

    def groupId(self):
        """Return the unique ID of the group this algorithm belongs to."""
        return ''

    def shortHelpString(self):
        """Return the display help of the algortihm."""
        return self.tr(
            """
            Extract the edges of polygon layer geometries and create new \
                polygons with the edges buffered to fill a width.
            The width of the output polygon must be expressed in tenths of \
                milimiter.
            """
        )

    def shortDescription(self):
        """Return the display description of the algorithm."""
        return self.tr('Extract the edges of polygon layer geometries.')

    def initAlgorithm(self, config=None):
        """Define inputs and outputs of the algorithm."""
        # PARAMETERS
        input_param = QgsProcessingParameterVectorLayer(
            self.INPUT,
            self.tr('Input vector layer'),
            types=[QgsProcessing.TypeVectorAnyGeometry],
            defaultValue=None
        )
        self.addParameter(input_param)

        width_param = QgsProcessingParameterNumber(
            self.WIDTH,
            self.tr('Width of output edge.'),
            QgsProcessingParameterNumber.Integer,
            minValue=1,
            defaultValue=self.rw_settings('r', 'edge_width', 12)
        )
        self.addParameter(width_param)

        # OUTPUTS
        edges_output = QgsProcessingParameterFeatureSink(
            self.OUTPUT,
            self.tr('Edges'),
            QgsProcessing.TypeVectorAnyGeometry,
            defaultValue=QgsProcessing.TEMPORARY_OUTPUT
        )
        self.addParameter(edges_output)

    def processAlgorithm(self, parameters, context, feedback):
        """Extract edges process.

        Return a polygon layer with the edges of input layer buffered to \
            fill a width expressed in tenths of milimeter.
        """
        # Get parameters and write settings
        input_layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )
        edge_width = self.parameterAsInt(
            parameters,
            self.WIDTH,
            context
        )
        self.rw_settings('w', 'edge_width', edge_width)
        # Perform checks and processing
        # TODO: Check validity of input geometries.

        outputs = {}

        # Cast input geometries to singlepart.
        alg_params = {
            'INPUT': parameters[self.INPUT],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['singleparts'] = processing.run(
            'native:multiparttosingleparts',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # fix singlepart generated geometries.
        alg_params = {
            'INPUT': outputs['singleparts']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }

        outputs['fix_singleparts'] = processing.run(
            'native:fixgeometries',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Simplify to tenths of milimeter as minimum distance between vertices.
        alg_params = {
            'INPUT': outputs['fix_singleparts']['OUTPUT'],
            'METHOD': 0,  # Distance (Douglas-Peucker)
            'TOLERANCE': 1, # 0.0001 m.
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['simplify'] = processing.run(
            'native:simplifygeometries',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Fix simplified geometries.
        alg_params = {
            'INPUT': outputs['simplify']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['fix_simplified'] = processing.run(
            'native:fixgeometries',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Make the internal buffer.
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': - edge_width / 2.0,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['fix_simplified']['OUTPUT'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['buffer_int'] = processing.run(
            'native:buffer',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Fix internal buffer geometries.
        alg_params = {
            'INPUT': outputs['buffer_int']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['fix_bufferint'] = processing.run(
            'native:fixgeometries',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Make the external buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': edge_width / 2.0,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['fix_simplified']['OUTPUT'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['buffer_ext'] = processing.run(
            'native:buffer',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Fix external buffer geometries.
        alg_params = {
            'INPUT': outputs['buffer_ext']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['fix_bufferext'] = processing.run(
            'native:fixgeometries',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Make the difference between external and internal buffers.
        alg_params = {
            'INPUT': outputs['fix_bufferext']['OUTPUT'],
            'OVERLAY': outputs['fix_bufferint']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['diff_buffers'] = processing.run(
            'native:difference',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Dissolve the difference.
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['diff_buffers']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['dissolved'] = processing.run(
            'native:dissolve',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        if feedback.isCanceled():
            return {}

        # Fix dissolved geometries.
        alg_params = {
            'INPUT': outputs['dissolved']['OUTPUT'],
            'OUTPUT': parameters[self.OUTPUT]
        }
        outputs['fix_dissolved'] = processing.run(
            'native:fixgeometries',
            alg_params,
            context=context,
            feedback=None,
            is_child_algorithm=True
        )

        # OUTPUT
        last_layer = context.getMapLayer(outputs['fix_dissolved']['OUTPUT'])
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            last_layer.fields(),
            last_layer.wkbType(),
            last_layer.crs(),
        )

        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )

        features = last_layer.getFeatures()
        total = (100.0 / last_layer.featureCount()
                    if last_layer.featureCount()
                    else 0)

        for current, inFeat in enumerate(features):
            if feedback.isCanceled():
                break

            sink.addFeature(inFeat, QgsFeatureSink.Flag.FastInsert)
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

        # return {self.OUTPUT: outputs['fix_dissolved']['OUTPUT']}
