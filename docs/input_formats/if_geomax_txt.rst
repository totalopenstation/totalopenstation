.. _if_geomax_txt:

===========================
:mod:`geomax_txt` -- TXT
===========================

.. moduleauthor:: Enzo Cocca

.. versionadded:: 0.7

A simple comma-separated text format exported from Geomax total stations.
Each line contains one point with its coordinates and an optional description.

Data format
===========

Each line is a comma-separated record::

    id, x, y, z, description

Fields:

- **id**: Point identifier (text)
- **x**: Easting coordinate
- **y**: Northing coordinate
- **z**: Elevation
- **description**: Optional point description

Sample data
===========

::

    1,1000.000,2000.000,100.000,POINT1
    2,1001.500,2001.500,100.250,POINT2
    3,1003.200,2003.200,99.800,CORNER

Supported devices
=================

Geomax total stations that export in TXT format, including:

- Geomax Zoom series
- Geomax Zipp series
