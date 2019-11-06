.. _if_nikon_raw:

===============================================
:mod:`nikon_raw_v200` -- Nikon RAW format V2.00
===============================================

.. moduleauthor:: Stefano Costa
.. versionadded:: 0.3.3

This format contains polar data. It is the first polar format
supported by Total Open Station.

Nikon RAW Record Information
============================

Data are basically comma-separated values, but each row can have a
different format and number of fields. Recorded points are in rows
that start with the ``SS`` string, while fixed base points start with
the ``ST`` string.

Definitions
===========

Coordinate records
------------------
+------+---+----+---+---------+---+----------+---+---------+---+-----------+---+------+
| type | , | pt | , | (pt id) | , | northing | , | easting | , | elevation | , | code |
+------+---+----+---+---------+---+----------+---+---------+---+-----------+---+------+

:type: One of the following codes |br|
    UP Uploaded point  |br|
    MP Manually input point |br|
    CC Calculated coordinate |br|
    RE Resection point
:pt: Point number
:(pt id): (Point ID)
:northing: Northing of the coordinate
:easting: Easting of the coordinate
:elevation: Elevation of the coordinate
:code: Feature code

Station records
---------------
+----+---+-------+---+---------+---+------+---+---------+---+----+---+--------+---+------+
| ST | , | stnpt | , | (stnid) | , | bspt | , | (bs id) | , | hi | , | bsazim | , | bsha |
+----+---+-------+---+---------+---+------+---+---------+---+----+---+--------+---+------+

:ST: Station record identifier (fixed text)
:stnpt: Station point number
:(stn id): (Station ID)
:bspt: Backsight point number
:(bs id): (Backsight ID)
:hi: Height of instrument
:bsazim: Backsight azimuth
:bsha: Backsight horizontal angle

Control point records
---------------------
+----+---+----+---+---------+---+----+---+----+---+----+---+----+---+------+---+------+
| CP | , | pt | , | (pt id) | , | ht | , | sd | , | ha | , | va | , | time | , | code |
+----+---+----+---+---------+---+----+---+----+---+----+---+----+---+------+---+------+

:CP: Control point record identifier (fixed text)
:pt: Point number
:(pt id): (Point ID)
:ht: Height of target
:sd: Slope distance
:ha: Horizontal angle
:va: Vertical angle
:time: 24-hour time stamp
:code: Feature code

Sideshot records
----------------
+----+---+----+---+----+---+----+---+----+---+----+---+------+---+------+
| SS | , | pt | , | ht | , | sd | , | ha | , | va | , | time | , | code |
+----+---+----+---+----+---+----+---+----+---+----+---+------+---+------+

:SS: Sideshot record identifier (fixed text)
:pt: Point number
:ht: Height of target
:sd: Slope distance
:ha: Horizontal angle
:va: Vertical angle
:time: 24-hour time stamp
:code: Feature code

Stakeout records
----------------
+----+---+----+---+--------+---+----+---+----+---+----+---+----+---+------+---+
| SO | , | pt | , | (sopt) | , | ht | , | sd | , | ha | , | va | , | time | , |
+----+---+----+---+--------+---+----+---+----+---+----+---+----+---+------+---+

:SO: Stakeout record identifier (fixed text)
:pt: Recorded point number
:(sopt): (Original number of point staked)
:ht: Height of target
:sd: Slope distance
:ha: Horizontal angle
:va: Vertical angle
:time: 24-hour time stamp

F1 records
----------
+------+---+----+---+----+---+----+---+----+---+----+---+------+
| face | , | pt | , | ht | , | sd | , | ha | , | va | , | time |
+------+---+----+---+----+---+----+---+----+---+----+---+------+

:face: One of the following |br|
    F1 Shot taken using Face-1 (fixed text) |br|
    Shot taken using Face-1 for Station setup (fixed text) |br|
:pt: Point number
:ht: Height of target
:sd: Slope distance
:ha: Horizontal angle
:va: Vertical angle
:time: 24-hour time stamp

Comment/note records
--------------------
+----+---+------+
| CO | , | text |
+----+---+------+

:CO: Comment record identifier (fixed text)
:text: Comment text

Acknowledgements
================

Support for this format was added thanks to Cynthia Mascione,
Università di Siena.

.. seealso::

    `Information on Total Station Nivo Series - Nivo3.M and Nivo5.M manual <http://www.geoglobex.it/wp-content/uploads/2015/07/NIKON-Nivo-M-manuale.pdf>`_ |br|
    `Information on Total Station DTM-322 manual <http://www.mcesurvey.com/files/Nikon_DTM-322_Total_Station_Manual.pdf>`_ |br|
    Documentation for Nikon RAW v2.00 from unofficial sources
