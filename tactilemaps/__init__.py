# -*- coding: utf-8 -*-
"""Import the plugin."""
__copyright__ = '(C) 2023 by Laboratorio de Geociencias - FIE'
__email__ = 'geociencias@fie.undef.edu.ar'
__license__ = 'GPL version 3'

def classFactory(iface):  # pylint: disable=invalid-name
    """Factory method for the plugin object."""
    from tactilemaps.tactilemaps_plugin import TactileMapsPlugin  # pylint: disable=import-outside-toplevel
    return TactileMapsPlugin(iface)
