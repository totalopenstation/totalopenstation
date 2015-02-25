======================================
 :mod:`sokkia_sdr33` -- Sokkia SDR 33
======================================

.. module:: sokkia_sdr33
    :platform: any
    :synopsis: Read data in the Sokkia SDR33 format
.. moduleauthor:: Stefano Costa
.. versionadded:: 0.4

Sokkia SDR33 is a format used by older models such as Sokkia SET 5F.

The format supports is based on fixed-position fields, with one record per
line. SDR33 supports both polar (“raw”) measurements and cartesian
coordinates (Northing, Easting, Elevation).

The first four characters of a line are useful to separate the various
type of measurements:

- prism height is marked by code ``03NM``
- polar measurements are marked by the ``09F1`` code
- cartesian measurements are marked by ``08TP``
- base stations are marked by ``02TP``, because their coordinates are
  entered by hand as cartesian coordinates

It is uncommon for polar and cartesian measurements to be found in the
same dataset. 
