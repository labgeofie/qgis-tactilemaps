# Change Log

## [v0.3.1] - Unreleased

**Update Spanish translations.**

### Added

### Changed


## [v0.3.0] - 2025-05-30

**Include algorithms to extract edges, write Braille and rasterize map.**

### Added

- tactilemaps/processing/algorithms/extractedges_algorithm.py
- tactilemaps/processing/algorithms/writebraille_algorithm.py
- tactilemaps/processing/algorithms/rasterize_algorithm.py
- tactilemaps/processing/utils/braille.py
### Changed

- tactilemaps/metadata.txt: *v0.3.0*.
- Conform to Flake8.

## [v0.2.0] - 2023-04-23

**Include Scale vector layer algorithm**

### Added

- tactilemaps/processing/algorithms/computescale_algortihm.py

### Changed

- tactilemaps/metadata.txt: *v0.2.0*
- tactilemaps/tactilemaps_plugin.py: *include scalevectorlayer action and menu entry*
- tactilemaps/i18n/tactilemaps.pro: *translate scalevectorlayer algorithm*
- tactilemaps/i18n/tactilemaps_es.qm: *translate scalevectorlayer algorithm*
- tactilemaps/i18n/tactilemaps_es.ts: *translate scalevectorlayer algorithm*
- tactilemaps/processing/tactilemaps_provider.py: *include scalevectorlayer algorithm*
- tactilemaps/processing/algorithms/computescale_algortihm.py: *write computed scale to scalevectorlayer settings*

## [v0.1.0] - 2023-04-11

**Primera versión de prueba**

### Added

- tactilemaps/\_\_init__.py
- tactilemaps/metadata.txt
- tactilemaps/tactilemaps_plugin.py
- tactilemaps/i18n/tactilemaps.pro
- tactilemaps/i18n/tactilemaps_es.qm
- tactilemaps/i18n/tactilemaps_es.ts
- tactilemaps/processing/\_\_init__.py
- tactilemaps/processing/tactilemaps_provider.py
- tactilemaps/processing/algorithms/\_\_init__.py
- tactilemaps/processing/algorithms/computescale_algortihm.py
