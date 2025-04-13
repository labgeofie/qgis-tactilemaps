# -*- coding: utf-8 -*-
"""Tactile Maps Plugin for QGIS.

This package provides a QGIS plugin to assist in the creation of tactile maps.
It includes tools for generating digital elevation models from vector
geometries to print tactile maps.

Subpackages:
- tactilemaps.processing: Processing provider for tactile map creation tools.
- tactilemaps.processing.algorithms: Algorithms registered by the processing
provider.

Modules:
- tactilemaps.tactilemaps_plugin: Main plugin module. Includes the
TactileMapsPlugin class, which defines how the plugin is loaded into QGIS.

Functions:
- classFactory: Imports the plugin into the QGIS interface.

************************************************************************
    Name                : __init__.py
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


def classFactory(iface):  # pylint: disable=invalid-name # noqa: N802
    """Initialize a plugin instance with the QGIS interface.

    Args:
        iface: QGIS interface.

    Returns:
        TactileMapsPlugin: The plugin class instance.
    """
    from tactilemaps.tactilemaps_plugin import TactileMapsPlugin

    return TactileMapsPlugin(iface)
