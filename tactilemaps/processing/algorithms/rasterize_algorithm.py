"""Rasterize polygon layers by a field value.

************************************************************************
    Name                : rasterize_algorithm.py
    Date                : Jun 2025
    Copyright           : (C) 2023-2025 by Laboratorio de Geociencias - FIE
    Email               : geociencias@fie.undef.edu.ar
************************************************************************
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
************************************************************************
"""

import os
import numpy as np

from qgis.core import (
    Qgis,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterExtent,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterString,
    QgsRasterFileWriter,
    QgsVectorLayer,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QSettings,
    QVariant
)
import processing
from osgeo import gdal


class RasterizeMap(QgsProcessingAlgorithm):
    """Rasterize polygon layers by a field value."""

    INPUT_LAYERS = "INPUT_LAYERS"
    FIELD_NAME   = "FIELD_NAME"
    EXTENT       = "EXTENT"
    PIXEL_SIZE = "PIXEL_SIZE"
    OUTPUT_RASTER = "OUTPUT_RASTER"

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('RasterizeMap', string)

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
        return RasterizeMap()

    def name(self):
        """Return the algorithm name."""
        return 'rasterizemap'

    def displayName(self):
        """Return the algorithm display name."""
        return self.tr('Rasterize map')

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
            Rasterize polygon layers by a field value.
            All layers must have the same CRS and a field with the value \
                to be rasterized.
            All units are in tenths of milimeter.
            """
        )

    def shortDescription(self):
        """Return the display description of the algorithm."""
        return self.tr('Rasterize a map from polygon layers.')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                "Polygon layers",
                # QgsProcessing.TypeVectorPolygon in older releases
                layerType=Qgis.ProcessingSourceType.VectorPolygon,
                defaultValue=[]
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.FIELD_NAME,
                "Field name",
                defaultValue=self.rw_settings('r', 'field_name', "")
            )
        )

        self.addParameter(
            QgsProcessingParameterExtent(
                self.EXTENT,
                "Map extent",
                defaultValue=None
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PIXEL_SIZE,
                "Pixel size",
                type=Qgis.ProcessingNumberParameterType.Double,
                defaultValue=self.rw_settings('r', 'pixel_size', 1)
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                "Rasterized map"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        layer_list = self.parameterAsLayerList(
            parameters,
            self.INPUT_LAYERS,
            context
        )

        field_name = self.parameterAsString(
            parameters,
            self.FIELD_NAME,
            context
        )
        self.rw_settings('w', 'field_name', field_name)

        extent_map = self.parameterAsExtent(
            parameters,
            self.EXTENT,
            context
        )

        ps = self.parameterAsInt(
            parameters,
            self.PIXEL_SIZE,
            context
        )
        self.rw_settings('w', 'pixel_size', ps)

        if not layer_list:
            feedback.reportError(
                "There is not any layer selected to rasterize.",
                fatalError=True
            )

        validated_layers = []
        reference_crs = None
        for lyr in layer_list:
            if not isinstance(lyr, QgsVectorLayer):
                feedback.reportError(
                    f"Layer '{lyr.name()}' is not a vector layer.",
                    fatalError=True
                )
                return {}

            if lyr.geometryType() != QgsWkbTypes.PolygonGeometry:
                feedback.reportError(
                    f"Layer '{lyr.name()}' is not a polygon layer.",
                    fatalError=True
                )
                return {}

            if reference_crs is None:
                reference_crs = lyr.crs()
            else:
                if not reference_crs == lyr.crs():
                    feedback.reportError(
                        f"Layer '{lyr.name()}' has a different CRS ({lyr.crs().authid()}) "
                        f"than the first layer ({reference_crs.authid()}).",
                        fatalError=True
                    )
                    return {}

            idx = lyr.fields().indexFromName(field_name)
            if idx < 0:
                feedback.reportError(
                    f"Layer '{lyr.name()}' doesn't have a field '{field_name}'.",
                    fatalError=True
                )
                return {}

            fld = lyr.fields()[idx]
            if not fld.isNumeric():
                feedback.reportError(
                    f"Layer '{lyr.name()}' field '{field_name}' is not numeric.",
                    fatalError=True
                )
                return {}

            validated_layers.append(lyr)

        # Merge all layers into a single layer
        uri = f"MultiPolygon?crs={reference_crs.authid()}"
        mem_layer = QgsVectorLayer(uri, "merged_polygons", "memory")
        prov = mem_layer.dataProvider()

        prov.addAttributes([QgsField(field_name, QVariant.Double)])
        mem_layer.updateFields()

        total_feats = 0
        for lyr in validated_layers:
            feats = lyr.getFeatures()
            for feat in feats:
                # Field name will be the only attribute
                val = feat[field_name]
                g = feat.geometry()
                new_feat = QgsFeature(mem_layer.fields())
                new_feat.setGeometry(QgsGeometry(g))
                new_feat.setAttribute(field_name, val)
                prov.addFeature(new_feat)
                total_feats += 1
                if feedback.isCanceled():
                    return {}

        if total_feats == 0:
            feedback.reportError(
                "No features found in input layers.",
                fatalError=True
            )
        mem_layer.updateExtents()

        # Rasterize
        xmin = extent_map.xMinimum()
        xmax = extent_map.xMaximum()
        ymin = extent_map.yMinimum()
        ymax = extent_map.yMaximum()
        extent_str = f"{xmin},{xmax},{ymin},{ymax}"

        params_raster = {
            'INPUT': mem_layer,
            'FIELD': field_name,
            'BURN': 0,
            'USE_Z': False,
            'UNITS': 1, # 0=georeferenced units, 1=pixel size units
            'WIDTH': ps,
            'HEIGHT': ps,
            'EXTENT': extent_str,
            'NODATA': -32000,
            'OPTIONS': '',
            'DATA_TYPE': 5, # 0=Byte, 1=UInt16, 2=Int16, 3=UInt32, 4=Int32, 5=Float32, 6=Float64
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }

        rasterized = processing.run("gdal:rasterize", params_raster, context=context, feedback=feedback)
        rasterized_output = rasterized['OUTPUT']

        # Round
        rasterized_dataset = gdal.Open(rasterized_output, gdal.GA_ReadOnly)
        crs = rasterized_dataset.GetProjection()
        geotransform = rasterized_dataset.GetGeoTransform()
        arr = np.float32(rasterized_dataset.GetRasterBand(1).ReadAsArray())
        rasterized_dataset = None

        # TODO: Add parameters for kernel radius and sigma
        RADIUS = 5
        SIGMA = 1.0

        dist = np.linspace(-RADIUS, RADIUS, RADIUS*2+1)

        kernel = np.exp(-dist**2 / (2*SIGMA**2))

        kernel = kernel / kernel.sum()

        def apply_kernel(vector, kernel):
            return np.convolve(vector, kernel, mode='same')

        rounded_cols = np.apply_along_axis(apply_kernel, 0, arr, kernel)
        rounded_arr = np.apply_along_axis(apply_kernel, 1, rounded_cols, kernel)

        outputFile = self.parameterAsOutputLayer(
            parameters,
            self.OUTPUT_RASTER,
            context)

        output_format = QgsRasterFileWriter.driverForExtension(
            os.path.splitext(outputFile)[1]
        )

        rounded_dataset = gdal.GetDriverByName(output_format).Create(
            outputFile,
            rounded_arr.shape[1],
            rounded_arr.shape[0],
            1,
            gdal.GDT_Float32,
            options=['COMPRESS=LZW']
        )
        rounded_dataset.SetProjection(crs)
        rounded_dataset.SetGeoTransform(geotransform)
        rounded_dataset.GetRasterBand(1).WriteArray(rounded_arr)
        rounded_dataset.GetRasterBand(1).SetNoDataValue(-32000)
        rounded_dataset = None

        return {self.OUTPUT_RASTER: outputFile}
