# -*- coding: utf-8 -*-
"""Write a text in Braille.

************************************************************************
    Name                : writebraille_algorithm.py
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
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPoint,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingLayerPostProcessorInterface,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer
)
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QMetaType,
    QSettings
)
from qgis.PyQt.QtGui import QTransform

from tactilemaps.utils import braille


class WriteBraille(QgsProcessingAlgorithm):
    """Write Braille algorithm class."""

    TEXT = 'TEXT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('WriteBraille', string)

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
        return WriteBraille()

    def name(self):
        """Return the algorithm name."""
        return 'writebraille'

    def displayName(self):
        """Return the algorithm display name."""
        return self.tr('Write Braille')

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
            Write a text in Braille.
            The text is automatically converted to uppercase and can be
                single-line or multi-line.
            The text will be written with the origin point at X=0, Y=0,
                in the EPSG:3857 coordinate system.
            The output will have a single feature with a multipoint geometry.
            """
        )

    def shortDescription(self):
        """Return the display description of the algorithm."""
        return self.tr('Scale a vector layer.')

    def initAlgorithm(self, config=None):
        """Define inputs and outputs of the algorithm."""
        # PARAMETERS
        text_param = QgsProcessingParameterString(
            name=self.TEXT,
            description=self.tr('Input Text'),
            multiLine=True,
            defaultValue=self.rw_settings('r', 'text', "")
        )
        self.addParameter(text_param)

        # OUTPUT
        braille_output = QgsProcessingParameterFeatureSink(
            name=self.OUTPUT,
            description=self.tr('Braille'),
            type=QgsProcessing.TypeVectorAnyGeometry,
            defaultValue=QgsProcessing.TEMPORARY_OUTPUT
        )
        self.addParameter(braille_output)

    def processAlgorithm(self, parameters, context, feedback):
        """Write Braille process.

        Return the input text, in Braille, as a vector layer with one feature \
            and MultiPoint geometry, centered in the origin of coordinates \
            of EPSG:3857 CRS.
        """
        # Get parameters and write settings
        input_text = self.parameterAsString(
            parameters=parameters,
            name=self.TEXT,
            context=context
        )

        print(input_text)

        self.rw_settings('w', 'text', input_text)

        # Get Braille geometry
        geom, errors = braille.translate(input_text)
        if errors:
            msg = f"One or more not implemented characters:{errors}."
            feedback.pushWarning(msg)

        # OUTPUT
        fields = QgsFields()
        fields_list = [
            QgsField("id", QMetaType.Type.Int),
            QgsField("text", QMetaType.Type.QString),
        ]
        fields.append(fields_list)

        geometryType = Qgis.WkbType.MultiPoint
        crs = QgsCoordinateReferenceSystem("EPSG:3857")

        (sink, dest_id) = self.parameterAsSink(
            parameters=parameters,
            name=self.OUTPUT,
            context=context,
            fields=fields,
            geometryType=geometryType,
            crs=crs,
        )

        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(parameters, self.OUTPUT)
            )

        feat = QgsFeature(fields)
        feat["id"] = 1
        feat["text"] = input_text
        feat.setGeometry(geom)

        sink.addFeature(feat, QgsFeatureSink.Flag.FastInsert)

        return {self.OUTPUT: dest_id}
