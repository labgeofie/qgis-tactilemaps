# Mapas Táctiles
[(English version)]([#tactile-maps])

Complemento de QGIS con herramientas de procesamiento para **generar modelos digitales de elevación a partir de geometrías vectoriales**.

Incluye un calculador de escala, herramientas para escalar geometrías al tamaño del mapa impreso, extracción de contornos de polígonos, escritura Braille, rasterización y filtrado Gaussiano.

Desarrollo en el marco del *Proyecto de Desarrollo Tecnológico Y Social (PDTS–FIE): Mapas táctiles geográficos (3D) con fines educativos para personas con discapacidad visual*.

---

## Instalación

A partir de la versión 0.3.0, el complemento se encuentra publicado en el repositorio oficial de QGIS, por lo que se puede instalar la última versión directamente desde el [diálogo de complementos](https://docs.qgis.org/3.40/es/docs/user_manual/plugins/plugins.html#the-plugins-dialog).

También se puede descargar el archivo ZIP correspondiente a cualquiera de las [versiones publicadas en el sitio de complementos de QGIS](https://plugins.qgis.org/plugins/tactilemaps/#plugin-versions), haciendo click en el número de la versión que se quiere descargar, y dentro de la página de esa versión haciendo click en el botón de Descarga. El archivo descargado se instala en QGIS desde [la pestaña instalar a partir de ZIP](https://docs.qgis.org/3.40/es/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab).

También se publican en la página de [Lanzamientos](https://github.com/labgeofie/qgis-tactilemaps/releases) de este repositorio los archivos ZIP correspondientes a cada versión.

---

## Hoja de ruta a la versión 1.0.0

Las siguientes características serán incluídas antes de publicarse la primer versión estable.

- Algoritmos de procesamiento:
  - [x] Calcular escala
  - [x] Escalar capa vectorial
  - [x] Extraer contornos de polígonos
  - [x] Escribir Braille
  - [x] Rasterizar mapa
  - [x] Suavizar aristas

- Funciones del motor de expresiones:
  - [ ] computescale()
  - [ ] writebraille()

- [x] Crear el ícono del complemento.
- [ ] Documentar la [wiki](https://github.com/labgeofie/qgis-tactilemaps/wiki).
- [ ] Adjuntar un modelo gráfico que realice el flujo de trabajo completo utilizando las herramientas instaladas por el complemento, a partir una capa de polígonos hasta el mapa en formato raster para imprimir en 3D.

---

Copyright: (C) 2023-2025, Laboratorio de Geociencias - FIE

Licencia: [GNU General Public License, Version 3](https://raw.githubusercontent.com/labgeofie/qgis-tactilemaps/main/LICENSE)

---
*English version*
## Tactile Maps

QGIS plugin with processing tools to **generate digital elevation models from vector geometries**. 

Includes a scale calculator, tools for scaling geometries to the size of the printed map, extraction of polygon contours, Braille writing, rasterization, and Gaussian filtering. 

Development made under the framework of the *Proyecto de Desarrollo Tecnológico Y Social (PDTS–FIE): Mapas táctiles geográficos (3D) con fines educativos para personas con discapacidad visual* project.

### Instalation

As of version 0.3.0, the plugin is published in the official QGIS repository, so the latest version can be installed directly from the [plugins dialog](https://docs.qgis.org/3.40/en/docs/user_manual/plugins/plugins.html#the-plugins-dialog). 

The ZIP file corresponding to any of the [versions published on the QGIS plugin site](https://plugins.qgis.org/plugins/tactilemaps/#plugin-versions) can also be downloaded, by clicking on the number of the version to download, and within the page of that version by clicking on the Download button. The downloaded file is installed in QGIS from [install from ZIP tab](https://docs.qgis.org/3.40/en/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab). 

The ZIP files for each version are also published on the [Releases](https://github.com/labgeofie/qgis-tactilemaps/releases) page of this repository.