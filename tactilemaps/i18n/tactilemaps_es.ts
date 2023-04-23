<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="es" sourcelanguage="en">
<context>
    <name>ComputeScale</name>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="84"/>
        <source>Compute scale</source>
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
        <location filename="../processing/algorithms/computescale_algorithm.py" line="172"/>
        <source>Computed scale number</source>
        <translation>Número de escala calculada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/compute_scale.py" line="96"/>
        <source>Extent to scale</source>
        <translation type="obsolete">Extensión a escalar</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="126"/>
        <source>Width of the map (in millimeters)</source>
        <translation>Ancho del mapa (en milímetros)</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="134"/>
        <source>Height of the map (in millimeters)</source>
        <translation>Alto del mapa (en milímetros)</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="153"/>
        <source>Multiple to round the scale denominator</source>
        <translation>Múltiplo a redondear el denominador de escala</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/compute_scale.py" line="172"/>
        <source>CRS of the extent must be projected, but {authid} is a geographic CRS.</source>
        <translation type="obsolete">SRC de la extensión debe ser proyectado, pero {authid} es un SRC geográfico.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="96"/>
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
        <location filename="../processing/algorithms/computescale_algorithm.py" line="121"/>
        <source>Extent to compute scale</source>
        <translation>Extensión para calcular escala</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="142"/>
        <source>Margin percentage</source>
        <translation>Porcentaje de margen</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="165"/>
        <source>Computed extent</source>
        <translation>Extensión calculada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="222"/>
        <source>The CRS of the extent could not be                 determined or is invalid.</source>
        <translation>El sistema de referencia de la extensión no pudo determinarse o es inválido.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="231"/>
        <source>The CRS of the extent must be projected,                 but {authid} is a geographic CRS.</source>
        <translation>El SRC de la extensión debe ser proyectado, pero {authid} es un SRC geográfico.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/computescale_algorithm.py" line="114"/>
        <source>Compute the scale denominator for a map,             from an extent.</source>
        <translation>Calcula el denominador de escala para un mapa, a partir de una extensión.</translation>
    </message>
</context>
<context>
    <name>ScaleVectorLayer</name>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="74"/>
        <source>Scale vector layer</source>
        <translation>Escalar capa vectorial</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="86"/>
        <source>
            Scale a vector layer, from an extent layer, by a scale                 denominator number.
            The extent layer and the scale are typically                 the outputs of the Compute scale algorithm.
            Output layer will be scaled to the origin of                 coordinates of the EPSG:3857 Coordinates                 Reference System, and will measure the size of the                 map to print, in meters.
            EPSG:3857 CRS will be assigned to the                 output layer, without reprojecting it.
            </source>
        <translation>Escalar una capa vectorial, desde una capa de extensión, según un número denominador de escala.
La capa de extensión y la escala son generalmente las salidas del algoritmo Calcular escala.
La capa de salida será escalada al origen de coordenadas del Sistema de Referencia de Coordenadas EPSG:3857, y medirá el tamaño del mapa a imprimir, en metros.
El SRC EPSG:3857 se asignará a la capa de salida, sin reproyectarla.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="103"/>
        <source>Scale a vector layer.</source>
        <translation>Escalar una capa vectorial.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="108"/>
        <source>Input vector layer</source>
        <translation>Capa vectorial de entrada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="115"/>
        <source>Extent layer</source>
        <translation>Capa de extensión</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="122"/>
        <source>Scale denominator number</source>
        <translation>Número denominador de escala</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="131"/>
        <source>Scaled</source>
        <translation>Escalada</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="169"/>
        <source>The CRS of the input layer could not be                 determined or is invalid.</source>
        <translation>El SRC de la capa de entrada no pudo determinarse o es inválido.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="178"/>
        <source>The CRS of the extent layer could not be                 determined or is invalid.</source>
        <translation>El SRC de la capa de extensión no pudo determinarse o es inválido.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="187"/>
        <source>The CRS of the input layer must be                 projected, but {input_authid} is a geographic CRS.</source>
        <translation>El SRC de la capa de entrada debe ser proyectado, pero {input_authid} es un SRC geográfico.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="196"/>
        <source>The CRS of the extent layer must be                 projected, but {extent_authid} is a geographic CRS.</source>
        <translation>El SRC de la capa de extensión debe ser proyectado, pero {extent_authid} es un SRC geográfico.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="205"/>
        <source>The CRS of the input layer ({input_authid})                 is not the same as the CRS of the extent layer                 ({extent_authid}).</source>
        <translation>El SRC de la capa de entrada ({input_authid}) no es el mismo que el SRC de la capa de extensión ({extent_authid}).</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="219"/>
        <source>The extent layer has not a valid extent.</source>
        <translation>La capa de extensión no tiene una extensión válida.</translation>
    </message>
    <message>
        <location filename="../processing/algorithms/scalevectorlayer_algorithm.py" line="265"/>
        <source>Scaled_{input_layer_name}</source>
        <translation>Escalada_{input_layer_name}</translation>
    </message>
</context>
<context>
    <name>TactileMapsPlugin</name>
    <message>
        <location filename="../tactilemaps_plugin.py" line="64"/>
        <source>&amp;Compute scale</source>
        <translation>&amp;Calcular escala</translation>
    </message>
    <message>
        <location filename="../tactilemaps_plugin.py" line="94"/>
        <source>&amp;Tactile Maps</source>
        <translation>Mapas &amp;Táctiles</translation>
    </message>
    <message>
        <location filename="../tactilemaps_plugin.py" line="71"/>
        <source>&amp;Scale vector layer</source>
        <translation>E&amp;scalar capa vectorial</translation>
    </message>
</context>
<context>
    <name>TactileMapsProvider</name>
    <message>
        <location filename="../processing/tactilemaps_provider.py" line="43"/>
        <source>Tactile maps</source>
        <translation>Mapas táctiles</translation>
    </message>
</context>
</TS>
