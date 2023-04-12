# -*- coding: utf-8 -*-
__copyright__ = '(C) 2023 by Laboratorio de Geociencias - FIE'
__email__ = 'geociencias@fie.undef.edu.ar'
__license__ = 'GPL version 3'

def classFactory(iface):
    """Factory method for the plugin object."""
    from tactilemaps.tactilemaps_plugin import TactileMapsPlugin
    return TactileMapsPlugin(iface)

