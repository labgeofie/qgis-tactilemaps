# -*- coding: utf-8 -*-
"""
************************************************************************
    Name                : tactilemaps_plugin.py
    Date                : March 2023
    Copyright           : (C) 2023 by Laboratorio de Geociencias - FIE
    Email               : geociencias@fie.undef.edu.ar
************************************************************************
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
************************************************************************
"""

import os

from qgis import processing
from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator
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
        # Init actions
        self.computescale_action = QAction(
            self.tr('&Compute Scale'),
            self.iface.mainWindow()
        )
        # Connect actions to run methods
        self.computescale_action.triggered.connect(
            self.run_computescale
        )
        # Init menu
        self.menu = QMenu(self.tr('&Tactile Maps'))
        self.menu.addActions([
            self.computescale_action
        ])
        self.iface.pluginMenu().addMenu(self.menu)
        # Init Processing
        self.initProcessing()

    def unload(self):
        """Remove menu entries and provider."""
        self.iface.removePluginMenu(
            self.tr('&Tactile Maps'),
            self.computescale_action
        )
        QgsApplication.processingRegistry().removeProvider(self.provider)

    def run_computescale(self):
        """Open the Compute Scale algorithm dialog."""
        processing.execAlgorithmDialog('tactilemaps:computescale')
