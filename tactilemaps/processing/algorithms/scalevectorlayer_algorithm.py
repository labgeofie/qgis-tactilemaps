# -*- coding: utf-8 -*-
"""Scale a vector layer given a scale denominator number.

************************************************************************
    Name                : scalevectorlayer_algorithm.py
    Date                : April 2023
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


class ScaleVectorLayer(QgsProcessingAlgorithm):
    """Scale vector layer algorithm class."""

    INPUT = 'INPUT'
    EXTENT = 'EXTENT'
    SCALE = 'SCALE'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('ScaleVectorLayer', string)

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
        return ScaleVectorLayer()

    def name(self):
        """Return the algorithm name."""
        return 'scalevectorlayer'

    def displayName(self):
        """Return the algorithm display name."""
        return self.tr('Scale vector layer')

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
            Scale a vector layer, from an extent layer, by a scale \
                denominator number.
            The extent layer and the scale are typically \
                the outputs of the Compute scale algorithm.
            Output layer will be scaled to the origin of \
                coordinates of the EPSG:3857 Coordinates \
                Reference System, and will measure the size of the \
                map to print, in tenths of milimeter.
            EPSG:3857 CRS will be assigned to the \
                output layer, without reprojecting it.
            """
        )

    def shortDescription(self):
        """Return the display description of the algorithm."""
        return self.tr('Scale a vector layer.')

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
        extent_param = QgsProcessingParameterVectorLayer(
            self.EXTENT,
            self.tr('Extent layer'),
            types=[QgsProcessing.TypeVectorPolygon],
            defaultValue=None
        )
        self.addParameter(extent_param)
        scale_param = QgsProcessingParameterNumber(
            self.SCALE,
            self.tr('Scale denominator number'),
            QgsProcessingParameterNumber.Integer,
            minValue=1,
            defaultValue=self.rw_settings('r', 'scale', 1)
        )
        self.addParameter(scale_param)
        # OUTPUTS
        scaled_output = QgsProcessingParameterFeatureSink(
            self.OUTPUT,
            self.tr('Scaled'),
            QgsProcessing.TypeVectorAnyGeometry,
            defaultValue=QgsProcessing.TEMPORARY_OUTPUT
        )
        self.addParameter(scaled_output)

    def processAlgorithm(self, parameters, context, feedback):
        """Scale Vector Layer process.

        Return the input vector layer scaled, from the extent layer,
            by a scale denominator number, centered in the origin of
            coordinates of EPSG:3857.
        """
        # Get parameters and write settings
        input_layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )
        extent_layer = self.parameterAsVectorLayer(
            parameters,
            self.EXTENT,
            context
        )
        scale_number = self.parameterAsInt(
            parameters,
            self.SCALE,
            context
        )
        self.rw_settings('w', 'scale', scale_number)
        # Perform checks and processing
        input_crs = input_layer.crs()
        input_authid = input_crs.authid()
        extent_crs = extent_layer.crs()
        extent_authid = extent_crs.authid()
        if not input_crs.isValid():
            msg = self.tr(
                'The CRS of the input layer could not be \
                determined or is invalid.'
            )
            feedback.reportError(
                msg,
                fatalError=True
            )
            return {}
        if not extent_crs.isValid():
            msg = self.tr(
                'The CRS of the extent layer could not be \
                determined or is invalid.'
            )
            feedback.reportError(
                msg,
                fatalError=True
            )
            return {}
        if input_crs.isGeographic():
            msg = self.tr(
                'The CRS of the input layer must be \
                projected, but {input_authid} is a geographic CRS.'
            )
            feedback.reportError(
                msg.format(input_authid=input_authid),
                fatalError=True
            )
            return {}
        if extent_crs.isGeographic():
            msg = self.tr(
                'The CRS of the extent layer must be \
                projected, but {extent_authid} is a geographic CRS.'
            )
            feedback.reportError(
                msg.format(extent_authid=extent_authid),
                fatalError=True
            )
            return {}
        if input_authid != extent_authid:
            msg = self.tr(
                'The CRS of the input layer ({input_authid}) \
                is not the same as the CRS of the extent layer \
                ({extent_authid}).'
            )
            feedback.reportError(
                msg.format(
                    input_authid=input_authid,
                    extent_authid=extent_authid
                ),
                fatalError=True
            )
            return {}
        extent_rectangle = extent_layer.extent()
        if extent_rectangle.isNull():
            msg = self.tr('The extent layer has not a valid extent.')
            feedback.reportError(
                msg,
                fatalError=True
            )
        input_fields = input_layer.fields()
        input_type = input_layer.wkbType()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            input_fields,
            input_type,
            QgsCoordinateReferenceSystem("EPSG:3857")
        )
        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )
        # Qtransform translates the scaled coordinates
        # 10000 is the tenths of milimeter to meters factor
        scale_factor = 10000/scale_number
        m11 = scale_factor
        m12 = 0.0
        m21 = 0.0
        m22 = scale_factor
        dx = -extent_rectangle.center().x() * scale_factor  # *
        dy = -extent_rectangle.center().y() * scale_factor  # *
        transformer = QTransform(m11, m12, m21, m22, dx, dy)
        # Transform each geometry and add feature to the sink
        partial_progress = 100
        if input_layer.featureCount() > 0:
            partial_progress = 100 / input_layer.featureCount()
        features = input_layer.getFeatures()
        for enum, feature in enumerate(features, 1):
            if feedback.isCanceled():
                return {}
            geom = feature.geometry()
            geom.transform(transformer)
            feature.setGeometry(geom)
            sink.addFeature(feature, QgsFeatureSink.FastInsert)
            feedback.setProgress(int(enum * partial_progress))
        return {self.OUTPUT: dest_id}
