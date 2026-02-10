.. _if_topcon_ascii:

====================================
:mod:`topcon_ascii` -- Topcon ASCII
====================================

.. moduleauthor:: Enzo Cocca

.. versionadded:: 0.7

A simple comma-separated text format exported from Topcon total stations.
Each line contains one point with its coordinates and an optional description.

Note that this format uses **Northing, Easting, Elevation** (Y, X, Z) ordering
in the file. The parser converts these to the internal X, Y, Z ordering.

Data format
===========

Each line is a comma-separated record::

    id, northing, easting, elevation, description

Fields:

- **id**: Point identifier (text)
- **northing**: Northing coordinate (Y)
- **easting**: Easting coordinate (X)
- **elevation**: Elevation (Z)
- **description**: Optional point description

Sample data
===========

::

    1,2000.000,1000.000,100.000,POINT1
    2,2001.500,1001.500,100.250,POINT2
    3,2003.200,1003.200,99.800,CORNER

Supported devices
=================

Topcon total stations that export in ASCII CSV format.
