# Mapas Táctiles

Complemento de QGIS con herramientas de procesamiento para **generar modelos digitales de elevación a partir de geometrías vectoriales**.

Incluye un calculador de escala, herramientas para escalar geometrías al tamaño del mapa impreso, extracción de contornos de polígonos, escritura Braille, rasterización y filtrado Gaussiano.

Desarrollo en el marco del *Proyecto de Desarrollo Tecnológico Y Social (PDTS–FIE): Mapas táctiles geográficos (3D) con fines educativos para personas con discapacidad visual*.

---

## Instalación

La publicación en el repositorio oficial de complementos de QGIS se realizará a partir de la primer versión estable (v1.0.0).

Actualmente el complemento está en estado de desarrollo y puede instalarse de dos maneras:

1. Agregando al listado de repositorios de complementos de QGIS:
   - En el menú *Complementos* de QGIS, abra el diálogo *Administrar e instalar complementos...*
   - En la pestaña *Configuración*, en la sección de *Repositorios de complementos*, presione el botón Añadir
   - En *Nombre*, elija un nombre que identifique al repositorio, por ejemplo: `Repositorio de Mapas Táctiles`.
   - En *URL*, ingrese la siguiente dirección: `https://github.com/labgeofie/qgis-tactilemaps/releases/latest/download/plugins.xml`
   - Al presionar *Aceptar*, el repositorio se agrega al listado de repositorios de complementos de QGIS, y podrá instalar el complemento desde la pestaña *Todos*.
   - **De esta forma, cada vez que se realice un nuevo lanzamiento, podrá actualizar el complemento sin necesidad de volver a instalarlo.**

2. Instalando una versión en particular desde un archivo zip.
   - Desde la página de [Lanzamientos](https://github.com/labgeofie/qgis-tactilemaps/releases), descargue el archivo `tactilemaps.x.y.z.zip` de la versión que desee instalar.
   - En el menú *Complementos* de QGIS, abra el diálogo *Administrar e instalar complementos...*
   - En la pestaña *Instalar a partir de zip*, presione *...* para abrir un explorador de archivos. Busque y seleccione el archivo zip descargado y presione *Abrir* en el explorador.
   - Por último, presione *Instalar complemento*

---

## Hoja de ruta a la versión 1.0.0

Las siguientes características serán incluídas antes de publicarse la primer versión estable.

- Algoritmos de procesamiento:
  - [x] Calcular escala
  - [ ] Escalar capa vectorial
  - [ ] Extraer contornos de polígonos
  - [ ] Escribir Braille
  - [ ] Rasterizar mapa
  - [ ] Suavizar aristas

- Funciones del motor de expresiones:
  - [ ] computescale()
  - [ ] writebraille()

- [ ] Crear el ícono del complemento.
- [ ] Documentar la [wiki del proyecto](https://github.com/labgeofie/qgis-tactilemaps/wiki).
- [ ] Adjuntar un modelo gráfico que realice el flujo de trabajo completo utilizando las herramientas instaladas por el complemento, a partir una capa de polígonos hasta el mapa en formato raster para imprimir en 3D.

---

Copyright: (C) 2023, Laboratorio de Geociencias - FIE

Licencia: [GNU General Public License, Version 3](https://raw.githubusercontent.com/labgeofie/qgis-tactilemaps/main/LICENSE)
