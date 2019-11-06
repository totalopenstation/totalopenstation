.. _Carlson website: http://update.carlsonsw.com/kbase_attach/372/

.. _if_carlson_rw5:

===============================================================
:mod:`carlson_rw5` -- Carlson SurvCE Raw Data File Format (RW5)
===============================================================

.. moduleauthor:: Stefano Costa, Filip Kłosowski
.. versionadded:: 0.4

Carlson RW5 is an exchange format used by the Carlson SurvCE software.

The official documentation about the format is provided on the
`Carlson website`_.

RW5 is a rich format for raw data about the entire field operation of total
stations and even GPS.

For example::

  OC,OP111,N 16556174.237,E 942130.662,EL 16.404
  BK,OP111,BP108,BS0.00000,BC0.00000 LS,HI5.684,HR5.500
  SS,OP111,FP108,AR0.00000,ZE0.00017,SD3.3566,--FENCE1
  
At the moment, a minimal subset of the specification is supported, consisting of
the ``OC``, ``BP``, ``LS`` and ``SS`` record types.

Carlson Record Information
==========================

The format is a comma separated ASCII file containing record types, headers,
recorded data and comments. The format is based on the :ref:`tds` raw data
specification with the exception of angle sets.

Angle sets are recorded as BD, BR, FD and FR records to allow reduction of all
possible data that can be recorded by SurvCE using the “Set Collection”
routine. Essentially, these records are identical to a sideshot record. With
the exception of the aforementioned angle set records, if the :ref:`tds`
specification is modified to provide enhanced functionality, the added or
modified data will reside in comment records to avoid incompatibility with
existing software.

Each record is made of one line of text, with comma-separated fields of ASCII
text format::

  AH,DC%s,MA%s,ME%s,RA%s

The first field is a two-letter code of the type of record. All the following
fields are composed with 1- or 2- letter field codes (such as ``OP``, ``N`` or
``FP``) and numeric values called an (ENUM). The “Notes” field is introduced by
the ``--`` code and contains a description of the record.

In practice, each point has a unique number and can be referenced for various
purposes from other records.

*Sideshot* records (``SS``) reference the *Occupy point* record in the``OP``
field. 

Record types
------------

+-------------+-----------------------------------------------+-----------------------+
| Record Type | Explanation                                   | Applicable for        |
+=============+===============================================+=======================+
| ``--`` *    | Note                                          | General Raw Data      |
+-------------+-----------------------------------------------+-----------------------+
| JB*         | Job                                           |                       |
+-------------+-----------------------------------------------+-----------------------+
| MO*         | Mode Setup                                    |                       |
+-------------+-----------------------------------------------+-----------------------+
| BD*         | Backsight Direct                              | Conventional Raw Data |
+-------------+-----------------------------------------------+-----------------------+
| BK*         | Backsight                                     |                       |
+-------------+-----------------------------------------------+-----------------------+
| BR*         | Backsight Reverse                             |                       |
+-------------+-----------------------------------------------+-----------------------+
| FD*         | Foresight Direct                              |                       |
+-------------+-----------------------------------------------+-----------------------+
| FR*         | Foresight Reverse                             |                       |
+-------------+-----------------------------------------------+-----------------------+
| GPS         | GPS Position in |br|                          |                       |
|             | Lat: dd.mmss |br|                             |                       |
|             | Lon: dd.mmss - Negative for West |br|         |                       |
|             | WGS84 Ellipsoid Elevation                     |                       |
+-------------+-----------------------------------------------+-----------------------+
| GS          | Reduced local coordinate from GPS record |br| |                       |
|             | and localization data                         |                       |
+-------------+-----------------------------------------------+-----------------------+
| LS*         | Line of Sight                                 |                       |
+-------------+-----------------------------------------------+-----------------------+
| OC*         | Occupy Point                                  |                       |
+-------------+-----------------------------------------------+-----------------------+
| OF          | Off Center Shot                               |                       |
+-------------+-----------------------------------------------+-----------------------+
| SP*         | Store Point                                   |                       |
+-------------+-----------------------------------------------+-----------------------+
| TR/SS*      | Traverse / Sideshot                           |                       |
+-------------+-----------------------------------------------+-----------------------+

\* implemented type

Field headers
-------------

+--------------+--------------------------------+----------------+
| Field header | Explanation                    | Applicable for |
+--------------+--------------------------------+----------------+
| AD           | Azimuth Direction |br|         |                |
|              | 0: North |br|                  |                |
|              | 1: South                       |                |
+--------------+--------------------------------+----------------+
| AL*          | Angle-Left                     |                |
+--------------+--------------------------------+----------------+
| AR*          | Angle-Right                    |                |
+--------------+--------------------------------+----------------+
| AU*          | Angle Unit |br|                |                |
|              | 0: 360° sexagesimal |br|       |                |
|              | 1: 400 gon                     |                |
+--------------+--------------------------------+----------------+
| AZ*          | Azimuth                        |                |
+--------------+--------------------------------+----------------+
| BC*          | Back Circle                    |                |
+--------------+--------------------------------+----------------+
| BP*          | Back Point                     |                |
+--------------+--------------------------------+----------------+
| BR*          | Bearing |br|                   |                |
|              | [N123.4500W]                   |                |
+--------------+--------------------------------+----------------+
| BS           | Backsight |br|                 |                |
|              | when back point is not defined |                |
+--------------+--------------------------------+----------------+
| CE*          | Change Elevation               |                |
+--------------+--------------------------------+----------------+
| DL*          | Deflection-Left                |                |
+--------------+--------------------------------+----------------+
| DR*          | Deflection-Right               |                |
+--------------+--------------------------------+----------------+
| DT           | Local Date |br|                |                |
|              | [MM-DD-YYYY]                   |                |
+--------------+--------------------------------+----------------+
| E*           | Easting |br|                   |                |
|              | [E space]                      |                |
+--------------+--------------------------------+----------------+
| EC           | Earth Curvature |br|           |                |
|              | 0: off |br|                    |                |
|              | 1: on                          |                |
+--------------+--------------------------------+----------------+
| EL*          | Elevation                      |                |
+--------------+--------------------------------+----------------+
| EO           | EDM Offset                     |                |
+--------------+--------------------------------+----------------+
| FE           | Foresight Elevation            |                |
+--------------+--------------------------------+----------------+
| FP*          | Foresight Point                |                |
+--------------+--------------------------------+----------------+
| HD*          | Horizontal Distance            |                |
+--------------+--------------------------------+----------------+
| HI*          | Height of Instrument           |                |
+--------------+--------------------------------+----------------+
| HR*          | Height of Rod                  |                |
+--------------+--------------------------------+----------------+
| N            | Northing |br|                  |                |
|              | [N space]                      |                |
+--------------+--------------------------------+----------------+
| OC           | Occupy Point                   |                |
+--------------+--------------------------------+----------------+
| OP           | Occupy Point                   |                |
+--------------+--------------------------------+----------------+
| PN           | Point Number                   |                |
+--------------+--------------------------------+----------------+
| SD*          | Slope Distance                 |                |
+--------------+--------------------------------+----------------+
| SF           | Scale Factor                   |                |
+--------------+--------------------------------+----------------+
| TM           | Local Time |br|                |                |
|              | [HH:MM:SS]                     |                |
+--------------+--------------------------------+----------------+
| UN*          | Distance Unit |br|             |                |
|              | 0: feet |br|                   |                |
|              | 1: meter |br|                  |                |
|              | 2: US feet                     |                |
+--------------+--------------------------------+----------------+
| VA*          | Vertical Angle                 |                |
+--------------+--------------------------------+----------------+
| ZE*          | Zenith                         |                |
+--------------+--------------------------------+----------------+
| ``--``       | Note                           |                |
+--------------+--------------------------------+----------------+

\* Filed implemented

Definitions
===========

Backsight Record
----------------
:Record type: BK
:Field headers: 
   OP Occupy point |br|
   BP Back Point |br|
   BS Backsight |br|
   BC Back Circle
:Sample(s):
  ::

    BK,OP1,BP2,BS315.0000,BC0.0044

Job Record
----------
:Record type: JB
:Field headers: 
   NM Job name |br|
   DT Date |br|
   TM Time
:Sample(s):
  ::

    JB,NMSAMPLE,DT06-27-2003,TM14:21:53

Line of Sight Record
--------------------
:Record type: LS
:Field headers: 
   HI Height of Instrument |br|
   HR Height of Rod
:Sample(s):
  ::

    LS,HI5.000000,HR6.000000
    LS,HR4.000000

Mode Setup Record
-----------------
The mode setup will be recorded at the beginning of the raw data file.

:Record type: MO
:Field headers: 
   AD Azimuth direction |br|
   UN Distance unit |br|
   SF Scale factor |br|
   EC Earth Curvature |br|
   EO EDM offset |br|
   AU Angle Unit
:Sample(s):
  ::

    MO,AD0,UN0,SF1.00000000,EC1,EO0.0,AU0

Occupy Record
-------------
:Record type: OC
:Field headers: 
   PN Point number |br|
   N Northing |br|
   E Easting |br|
   EL Elevation |br|
   ``--`` Note
:Sample(s):
  ::

    OC,OP1,N 5000.00000,E 5000.00000,EL100.000,--CP

Off Center Shot Record
----------------------
:Record type: OF
:Field headers: 
   AR Angle right |br|
   ZE Zenith (actual) |br|
   SD Slope Distance
:Sample(s):
  ::

    OF,AR90.3333,ZE90.0000,SD25.550000
    OF,ZE90.3333,--Vert Angle Offset

Store Point Record
------------------
:Record type: SP
:Field headers: 
   PN Point Number |br|
   N Northing |br|
   E Easting |br|
   EL Elevation |br|
   ``--`` Note
:Sample(s):
  ::

    SP,PN100,N 5002.0000,E 5000.0000,EL100.0000,--PP

Traverse / Sideshot Record / Backsight Direct / Backsight Reverse / Foresight Direct / Foresight Reverse
--------------------------------------------------------------------------------------------------------
:Record type: TR / SS / BD / BR / FD / FR
:Field headers: 
  OP Occupy Point |br|
  FP Foresight Point |br|
  (one of the following) |br|
  - AZ Azimuth |br|
  - BR Bearing |br|
  - AR Angle-Right |br|
  - AL Angle-Left |br|
  - DR Deflection-Right |br|
  - DL Deflection-Left
  (one of the following) |br|
  - ZE Zenith |br|
  - VA Vertical angle |br|
  - CE Change Elevation |br|
  (one of the following) |br|
  - SD Slope Distance |br|
  - HD Horizontal Distance |br|
  ``--`` Note
:Sample(s):
  ::

    TR,OP1,FP4,AR90.3333,ZE90.3333,SD25.550000,--CP
    SS,OP1,FP2,AR0.0044,ZE86.0133,SD10.313750,--CP
    BD,OP1,FP2,AR0.0055,ZE86.0126,SD10.320000,--CP
    BR,OP1,FP2,AR180.0037,ZE273.5826,SD10.315000,--CP
    FD,OP1,FP3,AR57.1630,ZE89.4305,SD7.393000,--CP
    FR,OP1,FP3,AR237.1612,ZE270.1548,SD7.395000,--CP

TOPS is capable of converting raw measurement data into local coordinates, by
performing a sequential processing of all records in their order.

Known limitations
=================

Support for measurements is still incomplete, here is a list of **TODO**:
  * add all missing code
  * get comments
  * add the possibility to customize code

.. seealso::

  `Information on Carlson RW5  <http://web.carlsonsw.com/files/knowledgebase/kbase_attach/372/Info%20-%20SurvCE%20RW5%20Format.pdf>`_ |br|
  `Carlson RW5 format <http://web.carlsonsw.com/files/knowledgebase/kbase_attach/223/SurvCE%20RW5%20Format.pdf>`_ |br|
  Documentation for Carlson RW5 from Carlson knowledgebase.
  
