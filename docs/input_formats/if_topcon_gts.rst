.. _if_topcon_gts:

================================
:mod:`topcon_gts` -- Topcon GTS
================================

.. moduleauthor:: Stefano Costa, Enzo Cocca

Polar format from Topcon GTS series total stations. The parser handles
multiple data variations including serial-downloaded data (which may
contain communication artifacts) and clean exported data.

Polar measurements (horizontal angle, vertical angle, slope distance)
are automatically converted to Cartesian coordinates.

Data format
===========

Data downloaded via serial connection is a continuous stream of records,
separated by commas. Each record contains polar measurement data with
specific field markers. The raw serial data may include communication
artifacts (leading/trailing control characters, checksum digits at
line boundaries).

Serial download format (excerpt from a GTS-229 download)::

    _'_(_)1.540_+1_ ?+00043575m0970930+1317260g+00043530t**+00+00111_*_
    ,1.500_+2_ ?+00064702m0968990+1360970g+00064625t**+00+00099_*0048

Each record contains the following fields:

+------------------+-----------------------------------------------+
| Field            | Description                                   |
+==================+===============================================+
| Target height    | Height of the prism/reflector (e.g. ``1.540``) |
+------------------+-----------------------------------------------+
| Point ID         | Preceded by ``+`` (e.g. ``+1``, ``+2``)       |
+------------------+-----------------------------------------------+
| Slope distance   | Marked with ``m`` suffix (e.g. ``00043575m``)  |
+------------------+-----------------------------------------------+
| Vertical angle   | First angle value (e.g. ``0970930``)           |
+------------------+-----------------------------------------------+
| Horizontal angle | Marked with ``g`` suffix (e.g. ``1317260g``)   |
+------------------+-----------------------------------------------+
| Height diff      | Marked with ``t`` suffix (e.g. ``00043530t``)  |
+------------------+-----------------------------------------------+
| Description      | Optional text at the end of the record         |
+------------------+-----------------------------------------------+

Angle values are in gradians (gon), scaled by 10000.
Distance values are in millimeters.

Parsing strategies
==================

The parser uses three fallback strategies to handle format variations:

1. **Serial format**: Handles data downloaded directly from the instrument,
   including communication artifacts (leading/trailing characters, checksum
   digits at line boundaries)
2. **Clean format**: Handles properly exported data files
3. **Flexible format**: Regex-based pattern matching for non-standard variations

Coordinate conversion
=====================

Polar measurements are converted to Cartesian (NEZ) coordinates using:

- Base point: instrument position
- Angle unit: gradians (gon)
- Distance type: slope distance

Supported devices
=================

- Topcon GTS series total stations (GTS-210, GTS-220, GTS-229, GTS-230, etc.)
