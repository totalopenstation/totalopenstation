.. _if_trimble_dc:

==========================================
:mod:`trimble_dc` -- Trimble Data Collector
==========================================

.. moduleauthor:: Enzo Cocca

.. versionadded:: 0.7

Fixed-width format used by Trimble data collectors. Measurement records
are identified by the ``69TM`` record type marker.

Coordinates are stored in **Northing, Easting, Elevation** order.

Data format
===========

Each point line uses fixed-width fields::

    69TM<id>                <northing>     <easting>      <elevation><description>

Field positions:

- **Bytes 0-3**: Record type marker (``69TM``)
- **Bytes 4-19**: Point identifier (16 characters)
- **Bytes 20-35**: Northing coordinate (16 characters)
- **Bytes 36-50**: Easting coordinate (15 characters)
- **Bytes 51-67**: Elevation (17 characters)
- **Bytes 68-83**: Description (16 characters)

Sample data
===========

::

    69TM1                    2000.000000    1000.000000       100.000000POINT1
    69TM2                    2001.500000    1001.500000       100.250000POINT2

Supported devices
=================

Trimble data collectors that export in DC format.
