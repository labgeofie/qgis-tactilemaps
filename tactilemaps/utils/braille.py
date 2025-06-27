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
    QgsMultiPoint,
    QgsPoint,
)

ALPHABET = {
    " ": "0",
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
    "ü": "1256",
    "1": "3456-1",
    "2": "3456-12",
    "3": "3456-14",
    "4": "3456-145",
    "5": "3456-15",
    "6": "3456-124",
    "7": "3456-1245",
    "8": "3456-125",
    "9": "3456-24",
    "0": "3456-245",
    ".": "3",
    ",": "2",
    ";": "23",
    ":": "25",
    "¿": "26",
    "?": "26",
    "¡": "235",
    "!": "235",
    '"': "236",
    "'": "6-236",
    "(": "126",
    ")": "345",
    "[": "12356",
    "]": "23456",
    "{": "5-123",
    "}": "456-2",
    "-": "36",
    "—": "36-36",
    "*": "35",
    "/": "6-2",
    "\\": "5-3",
    "<": "5-13",
    ">": "46-2",
    "+": "235",
    "=": "2356",
    "%": "456-356",
    "&": "6-12346",
    "@": "5",
    "€": "456-15",
    "$": "456-234",
    "º": "356"
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

# Standard dimension parameters (tenths of milimeter).
DIM = {
    "a": 24,
    "b": 24,
    "c": 60,
    "d": 100,
    "e": 12,
    "f": 4  # Between 2 and 5, per "Documento técnico B1".
}

def convert_char(char):
    """Convert a character to a Braille list of arrays.

    Each array contains the mask for a Braille cell.
    If `char` isn't implemented, returns None.
    """
    # Uppercase implementation.
    if char.isalpha() and char.isupper():
        key = char.lower()
        base = ALPHABET.get(key)
        if base is None:
            return None
        sign = "46-" + base

    # Lowercase.
    else:
        sign = ALPHABET.get(char)
        if sign is None:
            return None

    # Split for multi-cell characters.
    cells = sign.split("-")
    list_of_arrs = []
    for cell in cells:
        char_arr = [[0, 0] for _ in range(3)]
        for dot in cell:
            if dot in POS:
                i, j = POS[dot]
                char_arr[i][j] = 1
        list_of_arrs.append(char_arr)

    return list_of_arrs

def create_points(char_arr, x_off=0, y_off=0):
    """Create a MultiPoint geometry from Braille array."""
    step_x = DIM["a"]
    step_y = DIM["b"]

    # Create points.
    points = []
    for i, row in enumerate(char_arr):
        for j, val in enumerate(row):
            if val:
                x = x_off + j * step_x
                y = y_off + (2 - i) * step_y
                points.append(QgsPoint(x, y))

    return points

def translate(text):
    """Translate a text to braille points.

    Return a tuple of a MultiPoint geometry (or None) and a
    (possibly empty) list of not implemented characters.
    """
    all_points = []
    errors = []

    # Process each line
    for row_idx, line in enumerate(text.splitlines()):
        y_off = - row_idx * DIM["d"]

        # Track cell index for multicell characters
        cell_idx = 0
        for char in line:
            char_cells = convert_char(char)
            if not char_cells:
                errors.append(char)
                continue

            for _cell in char_cells:
                x_off = cell_idx * DIM["c"]
                points = create_points(_cell, x_off, y_off)
                all_points.extend(points)
                cell_idx += 1

    multipoints = None
    if all_points:
        multipoints = QgsMultiPoint(all_points)

    return multipoints, errors
