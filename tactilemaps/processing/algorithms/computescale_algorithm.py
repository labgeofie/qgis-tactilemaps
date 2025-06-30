# -*- coding: utf-8 -*-
"""Compute the scale denominator for a map, from an extent and a map size.

************************************************************************
    Name                : computescale_algorithm.py
    Date                : March 2023
    Copyright           : (C) 2023-2025 by Laboratorio de Geociencias - FIE
    Email               : geociencias@fie.undef.edu.ar
************************************************************************
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
************************************************************************
"""

from math import ceil

from qgis.core import (
    QgsGeometry,
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputNumber,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsRectangle,
    QgsUnitTypes,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QSettings,
    QMetaType
)


class ComputeScale(QgsProcessingAlgorithm):
    """Compute Scale algorithm class."""

    INPUT = 'INPUT'
    WIDTH = 'WIDTH'
    HEIGHT = 'HEIGHT'
    MARGIN = 'MARGIN'
    MULTIPLE = 'MULTIPLE'
    OUTPUT = 'OUTPUT'
    SCALE = 'SCALE'

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('ComputeScale', string)

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
        """Create a new instance of the algorithm."""
        return ComputeScale()

    def name(self):
        """Define the algorithm name."""
        return 'computescale'

    def displayName(self):
        """Define the algorithm display name."""
        return self.tr('Compute scale')

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
            Compute the scale denominator for a map, from an extent.
            The extent input must have a projected CRS.
            The width and height of the map are assumed in tenths of \
                millimeters.
            The extent input can be extended by a margin percentage.
            The scale denominator is rounded to a multiple. Set it \
                to 1 to avoid rounding.
            This algorithm returns a vector layer with the extent \
                adjusted for the computed scale.
            The scale denominator number is also an output of the \
                algorithm, and will be in a field of the computed \
                extent layer.
            """
        )

    def shortDescription(self):
        """Return the display description of the algorithm."""
        return self.tr('Compute the scale denominator for a map, \
            from an extent.')

    def initAlgorithm(self, config=None):
        """Define inputs and outputs of the algorithm."""
        advanced_flag = QgsProcessingParameterDefinition.FlagAdvanced

        # PARAMETERS
        extent_param = QgsProcessingParameterExtent(
            self.INPUT,
            self.tr('Extent to compute scale')
        )
        self.addParameter(extent_param)

        width_param = QgsProcessingParameterNumber(
            self.WIDTH,
            self.tr(r'Width of the map (in tenths of millimeters)'),
            QgsProcessingParameterNumber.Integer,
            minValue=1,
            defaultValue=self.rw_settings('r', 'width', 2100)
        )
        self.addParameter(width_param)
        height_param = QgsProcessingParameterNumber(
            self.HEIGHT,
            self.tr(r'Height of the map (in tenths of millimeters)'),
            QgsProcessingParameterNumber.Integer,
            minValue=1,
            defaultValue=self.rw_settings('r', 'height', 2970)
        )
        self.addParameter(height_param)
        margin_param = QgsProcessingParameterNumber(
            self.MARGIN,
            self.tr(r'Margin percentage'),
            QgsProcessingParameterNumber.Integer,
            minValue=0,
            defaultValue=self.rw_settings('r', 'margin', 0)
        )
        margin_param.setFlags(
            margin_param.flags() | advanced_flag
        )
        self.addParameter(margin_param)

        multiple_param = QgsProcessingParameterNumber(
            self.MULTIPLE,
            self.tr(r'Multiple to round the scale denominator'),
            QgsProcessingParameterNumber.Integer,
            minValue=1,
            defaultValue=self.rw_settings('r', 'multiple', 1)
        )
        multiple_param.setFlags(
            multiple_param.flags() | advanced_flag
        )
        self.addParameter(multiple_param)

        # OUTPUTS
        main_output = QgsProcessingParameterFeatureSink(
            self.OUTPUT,
            self.tr('Computed extent'),
            QgsProcessing.TypeVectorPolygon,
            defaultValue=QgsProcessing.TEMPORARY_OUTPUT
        )
        self.addParameter(main_output)
        scale_output = QgsProcessingOutputNumber(
            self.SCALE,
            self.tr('Computed scale number')
        )
        self.addOutput(scale_output)

    def processAlgorithm(self, parameters, context, feedback):
        """Compute Scale process.

        Return the extent, adjusted by the computed scale, in a vector
            layer with a 'scale' field.
        Also return the computed scale denominator number.
        """
        # Get parameters and write settings
        extent = self.parameterAsExtent(
            parameters,
            self.INPUT,
            context
        )
        crs = self.parameterAsExtentCrs(
            parameters,
            self.INPUT,
            context
        )
        width = self.parameterAsInt(
            parameters,
            self.WIDTH,
            context
        )
        self.rw_settings('w', 'width', width)
        height = self.parameterAsInt(
            parameters,
            self.HEIGHT,
            context
        )
        self.rw_settings('w', 'height', height)
        margin = self.parameterAsInt(
            parameters,
            self.MARGIN,
            context
        )
        self.rw_settings('w', 'margin', margin)
        multiple = self.parameterAsInt(
            parameters,
            self.MULTIPLE,
            context
        )
        self.rw_settings('w', 'multiple', multiple)
        # Perform checks and processing
        if not crs.isValid():
            msg = self.tr(
                'The CRS of the extent could not be \
                determined or is invalid.'
            )
            feedback.reportError(
                msg,
                fatalError=True
            )
            return {}
        if crs.isGeographic():
            msg = self.tr(
                'The CRS of the extent must be projected, \
                but {authid} is a geographic CRS.'
            )
            feedback.reportError(
                msg.format(authid=crs.authid()),
                fatalError=True
            )
            return {}
        fields = QgsFields()
        fields.append(QgsField('scale', QMetaType.Type.Int))
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            crs
        )
        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )
        if feedback.isCanceled():
            return {}
        # Compute multiplier from map units (mm^-1) to extent crs units
        crs_units = crs.mapUnits()
        # Get the unit factor from meters to CRS units and adjust to tenths
        #  of milimeter.
        units_factor = QgsUnitTypes.fromUnitToUnitFactor(
            QgsUnitTypes.DistanceMeters,
            crs_units
        ) / 10000.0
        # Compute map width and height in the units of the extent crs
        map_width = width * units_factor
        map_height = height * units_factor
        # Expand input extent to margin
        extent.scale(1 + margin/100)
        # Scale denominator without round
        scale = max(
            extent.width() / map_width,
            extent.height() / map_height
        )
        # Round (to a multiple) the scale denominator
        rounded_scale = multiple * ceil(scale/multiple)
        QSettings().setValue(
            'tactilemaps/scalevectorlayer/scale',
            rounded_scale
        )
        # Create feature, attribute and geometry
        feat = QgsFeature(fields)
        feat.setAttribute('scale', rounded_scale)
        rect_width = map_width * rounded_scale
        rect_height = map_height * rounded_scale
        rectangle = QgsRectangle.fromCenterAndSize(
            extent.center(),
            rect_width,
            rect_height
        )
        geom = QgsGeometry.fromRect(rectangle)
        feat.setGeometry(geom)
        sink.addFeature(feat, QgsFeatureSink.FastInsert)
        return {self.OUTPUT: dest_id, self.SCALE: rounded_scale}
