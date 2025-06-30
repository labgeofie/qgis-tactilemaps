#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create the zipfile to install plugin in QGIS.

The name of the created zip file will be tactilemaps_v<x>_<y>_<z>.zip,
where <x>.<y>.<z> is the version number of the plugin,
which is extracted from the metadata.txt file located in ./tactilemaps.
Inside the zip file there is a directory ./tactilemaps with the source code of
the plugin and the ./LICENSE file.
"""

import configparser
import pathlib
import shutil

def make():
    """Create the zipfile to install in QGIS."""

    # Define paths.
    this_path = pathlib.Path().resolve()
    src_path = this_path / 'tactilemaps'
    zipfiles_path = this_path / 'zipfiles'

    # Get the name and version of plugin.
    metadata = configparser.ConfigParser()
    metadata.read(src_path / 'metadata.txt')
    name = metadata['general']['name'].lower()
    version = metadata['general']['version']
    x_y_z = '_'.join(version.split('.'))

    zip_name = f'{name}_v{x_y_z}'

    release_path = zipfiles_path / name

    # Delete release_path if exists.
    if release_path.exists():
        print(f"Directory '{str(release_path)}' exists.")
        shutil.rmtree(release_path)
        print(f"Directory '{str(release_path)}' deleted.")

    # Copy the source path contents to release path.
    shutil.copytree(src=src_path,
                    dst=release_path,
                    ignore=shutil.ignore_patterns('__pycache__'))
    print(f"Copying the contents of '{str(src_path)}' to '{str(release_path)}'.")

    # Copy ./LICENSE.
    shutil.copyfile(src=this_path / 'LICENSE',
                    dst=release_path / 'LICENSE')
    print("LICENSE file copied.")

    # Write zip file.
    shutil.make_archive(base_name=zipfiles_path / zip_name,
                        format='zip',
                        root_dir=zipfiles_path,
                        base_dir=name)
    print("Zipfile made at:",
          f"'{str(zipfiles_path / zip_name)}.zip'")


    shutil.rmtree(release_path)
    print(f"'{str(release_path)}' directory deleted.")

if __name__ == "__main__":
    make()
