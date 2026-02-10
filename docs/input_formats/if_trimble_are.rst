.. _if_trimble_are:

=========================================
:mod:`trimble_are` -- Trimble AREA format
=========================================

.. moduleauthor:: Stefano Costa, Luca Bianconi, Alessandro Bezzi, Enzo Cocca

Trimble AREA is a format used by Trimble total stations. Data is stored as
ASCII text with key-value pairs, one per line. Each record contains coordinate
and metadata fields identified by numeric keys.

Data format
===========

Records are separated by the ``0=`` marker (when present) or by the ``5=``
point number field. Each record contains key-value pairs::

    0=Measured point
    5=3
    4=FIX
    6=0.000
    7=107.1313
    8=100.5089
    9=9.111
    37=497.857
    38=499.622
    39=1.348

Field keys:

+------+-------------------------------+
| Key  | Description                   |
+======+===============================+
| 0=   | Record separator / comment    |
+------+-------------------------------+
| 4=   | Point description / code      |
+------+-------------------------------+
| 5=   | Point number                  |
+------+-------------------------------+
| 6=   | Horizontal angle              |
+------+-------------------------------+
| 7=   | Vertical angle                |
+------+-------------------------------+
| 8=   | Zenith angle                  |
+------+-------------------------------+
| 9=   | Slope distance                |
+------+-------------------------------+
| 37=  | Northing (X)                  |
+------+-------------------------------+
| 38=  | Easting (Y)                   |
+------+-------------------------------+
| 39=  | Elevation (Z)                 |
+------+-------------------------------+

A point record is valid when it contains fields ``5=``, ``4=``, ``37=``,
``38=`` and ``39=``.

Format variants
===============

Two variants are supported:

- **With record separator**: Records are delimited by ``0=`` lines.
  This is the standard format for measured points.
- **Without record separator**: Records start directly with ``5=``.
  The parser handles this variant by splitting on the ``5=`` field.
