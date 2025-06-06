# -*- coding: utf-8 -*-
""" Tactile Maps Processing provider.

************************************************************************
    Name                : tactilemaps_provider.py
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessingProvider

from tactilemaps.processing.algorithms import (
    computescale_algorithm,
    scalevectorlayer_algorithm,
    extractedges_algorithm,
    writebraille_algorithm,
    rasterize_algorithm
)


class TactileMapsProvider(QgsProcessingProvider):
    """Tactile Maps provider class."""

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('TactileMapsProvider', string)

    def loadAlgorithms(self, *args, **kwargs):
        """Load the algorithms of the provider."""
        self.addAlgorithm(computescale_algorithm.ComputeScale())
        self.addAlgorithm(scalevectorlayer_algorithm.ScaleVectorLayer())
        self.addAlgorithm(extractedges_algorithm.ExtractEdges())
        self.addAlgorithm(writebraille_algorithm.WriteBraille())
        self.addAlgorithm(rasterize_algorithm.RasterizeMap())

    def id(self, *args, **kwargs):
        """Return the id of the provider."""
        return 'tactilemaps'

    def name(self, *args, **kwargs):
        """Return the display name of the provider."""
        return self.tr('Tactile maps')

    def icon(self):
        """Return the icon of the provider."""
        # TODO: Agregar un icono
        return QgsProcessingProvider.icon(self)
