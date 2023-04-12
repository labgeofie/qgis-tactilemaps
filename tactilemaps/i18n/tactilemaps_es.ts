<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="es" sourcelanguage="en">
<context>
    <name>ComputeScale</name>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="71"/>
        <source>Compute Scale</source>
        <translation>Calcular escala</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/compute_scale.py" line="79"/>
        <source>
            Compute the scale denominator for a map, from an extent.
            Extent CRS must be projected. If the extent does not have a CRS, it is assumed to be in meters.
            Width and height of the map are assumed in millimeters.
            The scale denominator is rounded to a multiple. Set it to 1 to avoid rounding.
            </source>
        <translation type="obsolete">Calcula el denominador de escala para un mapa, a partir de una extensión.
El SRC de la extensión debe ser proyectado. Si la extensión no tiene un SRC, se asume que está en metros.
Ancho y alto del mapa se asumen en milímetros.
El denominador de escala se redondea a un múltiplo. Defínalo como 1 para evitar el redondeo.
</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/compute_scale.py" line="139"/>
        <source>Computed scale</source>
        <translation type="obsolete">Escala calculada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="159"/>
        <source>Computed scale number</source>
        <translation>Número de escala calculada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/compute_scale.py" line="96"/>
        <source>Extent to scale</source>
        <translation type="obsolete">Extensión a escalar</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="113"/>
        <source>Width of the map (in millimeters)</source>
        <translation>Ancho del mapa (en milímetros)</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="121"/>
        <source>Height of the map (in millimeters)</source>
        <translation>Alto del mapa (en milímetros)</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="140"/>
        <source>Multiple to round the scale denominator</source>
        <translation>Múltiplo a redondear el denominador de escala</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/compute_scale.py" line="172"/>
        <source>CRS of the extent must be projected, but {authid} is a geographic CRS.</source>
        <translation type="obsolete">SRC de la extensión debe ser proyectado, pero {authid} es un SRC geográfico.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="83"/>
        <source>
            Compute the scale denominator for a map, from an extent.
            The extent input must have a projected CRS.
            The width and height of the map are assumed in millimeters.
            The extent input can be extended by a margin percentage.
            The scale denominator is rounded to a multiple. Set it                 to 1 to avoid rounding.
            This algorithm returns a vector layer with the extent                 adjusted for the computed scale.
            The scale denominator number is also an output of the                 algorithm, and will be in a field of the computed                 extent layer.
            </source>
        <translation>Calcula el denominador de escala para un mapa, a partir de una extensión.
La extensión de entrada debe tener un SRC proyectado.
El ancho y alto del mapa se asumen en milímetros.
La extensión de entrada se puede expandir según un porcentaje de margen.
El denominador de escala se redondea a un múltiplo. Defínalo como 1 para evitar el redondeo.
Este algoritmo devuelve una capa vectorial con la extensión ajustada según la escala calculada.
El número denominador de la escala también es una salida del algoritmo, y estará en un campo de la capa de extensión de salida.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="108"/>
        <source>Extent to compute scale</source>
        <translation>Extensión para calcular escala</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="129"/>
        <source>Margin percentage</source>
        <translation>Porcentaje de margen</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="152"/>
        <source>Computed extent</source>
        <translation>Extensión calculada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="209"/>
        <source>The CRS of the extent could not be                 determined or is invalid.</source>
        <translation>El sistema de referencia de la extensión no pudo determinarse o es inválido.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="217"/>
        <source>The CRS of the extent must be projected,                 but {authid} is a geographic CRS.</source>
        <translation>El SRC de la extensión debe ser proyectado, pero {authid} es un SRC geográfico.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="101"/>
        <source>Compute the scale denominator for a map,             from an extent.</source>
        <translation>Calcula el denominador de escala para un mapa, a partir de una extensión.</translation>
    </message>
</context>
<context>
    <name>TactileMapsPlugin</name>
    <message>
        <location filename="../tactilemaps_plugin.py" line="69"/>
        <source>&amp;Compute Scale</source>
        <translation>&amp;Calcular Escala</translation>
    </message>
    <message>
        <location filename="../tactilemaps_plugin.py" line="88"/>
        <source>&amp;Tactile Maps</source>
        <translation>Mapas &amp;Táctiles</translation>
    </message>
</context>
<context>
    <name>TactileMapsProvider</name>
    <message>
        <location filename="../processing/tactilemaps_provider.py" line="30"/>
        <source>Tactile Maps</source>
        <translation>Mapas Táctiles</translation>
    </message>
</context>
</TS>
