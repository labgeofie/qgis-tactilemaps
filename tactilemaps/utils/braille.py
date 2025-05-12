# -*- coding: utf-8 -*-
"""Utility functions to convert text to Braille.

************************************************************************
    Name                : braille.py
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

from qgis.core import (
    QgsPointXY,
    QgsGeometry
)

ALPHABET = {
    "a": "1",
    "b": "12",
    "c": "14",
    "d": "145",
    "e": "15",
    "f": "124",
    "g": "1245",
    "h": "125",
    "i": "24",
    "j": "245",
    "k": "13",
    "l": "123",
    "m": "134",
    "n": "1345",
    "ñ": "12456",
    "o": "135",
    "p": "1234",
    "q": "12345",
    "r": "1235",
    "s": "234",
    "t": "2345",
    "u": "136",
    "v": "1236",
    "w": "2456",
    "x": "1346",
    "y": "13456",
    "z": "1356",
    "á": "12356",
    "é": "2346",
    "í": "34",
    "ó": "346",
    "ú": "23456",
    "ü": "1256"
}

# Position (row, column) inside a 2x3 array for each point code.
POS = {
    '1': (0, 0),
    '2': (1, 0),
    '3': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1)
}

# Dimension parameters
DIM = {
    "a": 2.4,
    "b": 2.4
}

def convert_char(char):
    """Convert a character to a Braille array.

    The character can be lower or upper case.
    If not implemented, it returns None.
    """
    try:
        sign = ALPHABET[char]
    except KeyError:
        return None

    arr = [[0, 0] for _ in range(3)]

    for dot in sign:
        if dot in POS:
            i, j = POS[dot]
            arr[i][j] = 1

    return arr


def create_geom(arr):
    """Create a MultiPoint geometry from Braille array."""

    step_x = DIM["a"]
    step_y = DIM["b"]

    # Create points.
    points = []
    for i, row in enumerate(arr):
        for j, val in enumerate(row):
            if val:
                x = j * step_x
                y = (2 - i) * step_y
                points.append(QgsPointXY(x, y))

    return QgsGeometry.fromMultiPointXY(points)
