.. _if_trimble_jxl:

==========================================
:mod:`trimble_jxl` -- Trimble JobXML (JXL)
==========================================

.. moduleauthor:: Enzo Cocca

.. versionadded:: 0.7

Trimble JobXML (JXL) is an XML-based format used by Trimble total stations
and data collectors running Trimble Access or Trimble General Survey software.

The format stores survey data in a structured XML document containing point
records, station setups, polar observations, backsight data, instrument
metadata, and unit definitions.

Supported devices
=================

- Trimble C3, C5, M3, S series total stations
- Trimble data collectors running Trimble Access or Trimble General Survey

Data format
===========

A JXL file is an XML document with a ``<JOBFile>`` root element containing
a ``<FieldBook>`` section. The main record types are:

PointRecord
-----------

Contains point coordinates in ``<Grid>`` (keyed-in) or ``<ComputedGrid>``
(calculated from observations) elements. When both are present, ComputedGrid
is preferred as it includes applied corrections.

::

    <PointRecord ID="00000044" TimeStamp="2025-04-22T15:11:06">
        <Name>PQ_01</Name>
        <Code>POINT</Code>
        <Method>DirectReading</Method>
        <Classification>Normal</Classification>
        <Deleted>false</Deleted>
        <Circle>
            <HorizontalCircle>223.10809082876</HorizontalCircle>
            <VerticalCircle>92.075260416667</VerticalCircle>
            <EDMDistance>39.2598</EDMDistance>
            <Face>Face1</Face>
        </Circle>
        <ComputedGrid>
            <North>374311.24665733</North>
            <East>4128083.0148475</East>
            <Elevation>63.537665074073</Elevation>
        </ComputedGrid>
    </PointRecord>

StationRecord
-------------

Defines station setups with instrument height::

    <StationRecord ID="0000002b" TimeStamp="2025-04-22T15:06:28">
        <StationName>200</StationName>
        <TheodoliteHeight>1.635</TheodoliteHeight>
        <StationType>StationSetupPlus</StationType>
    </StationRecord>

UnitsRecord
-----------

Defines measurement units and coordinate order::

    <UnitsRecord ID="00000002" TimeStamp="2025-04-22T15:02:35">
        <DistanceUnits>Metres</DistanceUnits>
        <AngleUnits>DMSDegrees</AngleUnits>
        <CoordinateOrder>North-East-Elevation</CoordinateOrder>
    </UnitsRecord>

Coordinate handling
===================

The coordinate order is read from the ``<CoordinateOrder>`` element
(typically ``North-East-Elevation``).

For UTM projections, the parser detects and handles cases where Easting
and Northing values may be swapped in the ``<North>`` and ``<East>`` tags
by checking the magnitude of values (UTM Northing in Italy is typically
around 4,000,000 while Easting is below 1,000,000).

Parsing modes
=============

The parser supports two modes:

1. **Standard mode** (default): Reads coordinates directly from
   ``<Grid>`` or ``<ComputedGrid>`` elements.
2. **Celerimetric mode**: Recalculates coordinates from raw polar
   observations (horizontal angle, vertical angle, slope distance)
   using station and backsight data with known coordinates.

Extracted properties
====================

In addition to coordinates, the following properties are extracted
when available:

- **code**: Point code/description
- **classification**: Point classification (Normal, BackSight, etc.)
- **angle**: Horizontal circle reading
- **z_angle**: Vertical circle reading
- **slope_dist**: EDM slope distance
- **face**: Telescope face (Face1, Face2)
- **station_id**: Reference to the station setup
