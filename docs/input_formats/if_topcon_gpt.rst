.. _if_topcon_gpt:

================================
:mod:`topcon_gpt` -- Topcon GPT
================================

.. moduleauthor:: Enzo Cocca

.. versionadded:: 0.7

CSV text format exported from Topcon GPT series (Pulse Total Stations) via
Topcon Link software. GPT refers to the instrument series (GPT-3000,
GPT-3500, GPT-9000A, etc.), not to a file extension.

Point records are identified by the ``SD`` marker in each line. ``SD`` stands
for Slope Distance, a field from the Topcon raw data that is used here as
a record type identifier in the converted CSV output.

Coordinates are stored in **Northing, Easting, Elevation** (Y, X, Z) order.

Data format
===========

Each point line is a comma-separated record with an ``SD`` marker::

    id, SD, northing, easting, elevation

Fields:

- **id**: Point identifier
- **SD**: Record type marker (Slope Distance record)
- **northing**: Northing coordinate (Y)
- **easting**: Easting coordinate (X)
- **elevation**: Elevation (Z)

Sample data
===========

::

    1,SD,2000.0000000,1000.0000,100.0000
    2,SD,2001.5000000,1001.5000,100.2500
    3,SD,2003.2000000,1003.2000,99.80000

Supported devices
=================

- Topcon GPT series total stations (GPT-3000, GPT-3002, GPT-3003,
  GPT-3005, GPT-3007, GPT-3500, GPT-9000A)
