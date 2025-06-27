# -*- coding: utf-8 -*-
"""Tactile Maps Plugin for QGIS.

************************************************************************
    Name                : tactilemaps_plugin.py
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

import os
from pathlib import Path

from qgis import processing
from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

from tactilemaps.processing.tactilemaps_provider import (
    TactileMapsProvider
)


class TactileMapsPlugin:
    """Main plugin class."""

    def __init__(self, iface):
        """Init the plugin."""
        self.plugin_abspath = os.path.dirname(os.path.abspath(__file__))
        locale = QgsSettings().value(
            "locale/userLocale",
            QLocale().name()
        )
        qm_file = os.path.join(
            self.plugin_abspath,
            'i18n',
            f'tactilemaps_{locale}.qm'
        )
        self.translator = QTranslator()
        self.translator.load(qm_file)
        QCoreApplication.installTranslator(self.translator)
        self.iface = iface
        self.provider = None
        self.computescale_action = None
        self.menu = None

    def tr(self, string):
        """Return a localized string."""
        return QCoreApplication.translate('TactileMapsPlugin', string)

    def initProcessing(self):
        """Init processing provider."""
        self.provider = TactileMapsProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Init actions, run methods, menu entries and provider."""
        icon = QIcon(str(Path(__file__).parent / "icon.png"))
        # Init actions
        self.computescale_action = QAction(
            self.tr('&Compute scale'),
            self.iface.mainWindow()
        )
        self.computescale_action.triggered.connect(
            self.run_computescale
        )
        self.extractedges_action = QAction(
            self.tr('&Extract edges'),
            self.iface.mainWindow()
        )
        self.extractedges_action.triggered.connect(
            self.run_extractedges
        )
        self.rasterizemap_action = QAction(
            self.tr('&Rasterize map'),
            self.iface.mainWindow()
        )
        self.rasterizemap_action.triggered.connect(
            self.run_rasterizemap
        )
        self.writebraille_action = QAction(
            self.tr('&Write braille'),
            self.iface.mainWindow()
        )
        self.scalevectorlayer_action = QAction(
            self.tr('&Scale vector layer'),
            self.iface.mainWindow()
        )
        self.scalevectorlayer_action.triggered.connect(
            self.run_scalevectorlayer
        )
        self.writebraille_action.triggered.connect(
            self.run_writebraille
        )
        # Init menu
        self.menu = self.iface.pluginMenu().addMenu(
            icon,
            self.tr('&Tactile Maps')
        )
        self.menu.addActions([
            self.computescale_action,
            self.extractedges_action,
            self.rasterizemap_action,
            self.scalevectorlayer_action,
            self.writebraille_action
        ])

        # Init Processing
        self.initProcessing()

    def unload(self):
        """Remove menu entry and provider."""
        self.iface.pluginMenu().removeAction(self.menu.menuAction())
        QgsApplication.processingRegistry().removeProvider(self.provider)

    def run_computescale(self):
        """Open the Compute scale algorithm dialog."""
        processing.execAlgorithmDialog('tactilemaps:computescale')

    def run_extractedges(self):
        """Open the Extract edges algorithm dialog."""
        processing.execAlgorithmDialog('tactilemaps:extractedges')

    def run_rasterizemap(self):
        """Open the Rasterize map algorithm dialog."""
        processing.execAlgorithmDialog('tactilemaps:rasterizemap')

    def run_scalevectorlayer(self):
        """Open the Scale vector layer algorithm dialog."""
        processing.execAlgorithmDialog('tactilemaps:scalevectorlayer')

    def run_writebraille(self):
        """Open the Write braille algorithm dialog."""
        processing.execAlgorithmDialog('tactilemaps:writebraille')
