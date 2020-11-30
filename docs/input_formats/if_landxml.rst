.. _LandXML website: http://www.landxml.org/

.. _if_landxml:

=========================
:mod:`landxml` -- LandXML
=========================

.. moduleauthor:: Damien Gaignon
.. versionadded:: 0.6

LandXML is committed to providing an non-proprietary data standard (LandXML),
driven by an consortium of partners for the inter-operability of data utilized
within the Land Development industry.

The official documentation about the format is provided on the `LandXML website`_.

LandXML is a specialized XML (eXtensible Mark-up Language) data file format
containing civil engineering and survey measurement data commonly used in the
Land Development and Transportation Industries.

For example::

    <?xml version="1.0" encoding="utf-8"?>
    <LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2" time="15:49:09" date="2006-06-19" version="0" language="English" readOnly="false">
    <Units>
    <Metric linearUnit="meter" temperatureUnit="celsius" volumeUnit="cubicMeter" areaUnit="squareMeter" pressureUnit="milliBars" angularUnit="decimal dd.mm.ss" directionUnit="decimal dd.mm.ss">
    </Metric>
    </Units>
    <CgPoints>
    <CgPoint oID="2748159" state="existing" pntSurv="boundary" name="Q">312.04999999981374 274.33400000003166</CgPoint>
    <CgPoint oID="2748179" state="existing" pntSurv="boundary" name="W">308.8430000003427 277.0350000000326</CgPoint>
    <CgPoint oID="2746236" state="existing" pntSurv="boundary" name="M">306.9670000001788 19.508999999961816</CgPoint>
    </CgPoints>
    <Survey>
    <SurveyHeader name="IS185989" headOfPower="Survey and Mapping Infrastructure Act 2003" surveyFormat="Identification" surveyPurpose="Identification" desc="Plan of Identification Survey of Lots 26 &amp; 27 on RP726990 " type="surveyed" surveyStatus="Survey Records Only" fieldNoteFlag="false" submissionDate="2006-04-07" documentStatus="Captured">
    <CoordinateSystem horizontalDatum="Local" verticalDatum="Arbitrary" />
    </SurveyHeader>
    <InstrumentSetup id="IS-7-IS185989" stationName="7-IS185989" instrumentHeight="0">
    <InstrumentPoint pntRef="7-IS185989" />
    </InstrumentSetup>
    <InstrumentSetup id="IS-70-IS185989" stationName="70-IS185989" instrumentHeight="0">
    <InstrumentPoint pntRef="70-IS185989" />
    </InstrumentSetup>
    <ObservationGroup id="OG-1">
    <ReducedObservation name="3" setupID="IS-7-IS185989" targetSetupID="IS-70-IS185989" azimuth="302.504" horizDistance="10.81" distanceType="measured" azimuthType="measured" purpose="traverse" equipmentUsed="theodolite EDM" />
    <ReducedObservation name="6" setupID="IS-72-IS185989" targetSetupID="IS-73-IS185989" azimuth="110.274" horizDistance="37.55" distanceType="measured" azimuthType="measured" purpose="traverse" equipmentUsed="theodolite EDM" />
    <ReducedObservation name="4" setupID="IS-70-IS185989" targetSetupID="IS-71-IS185989" azimuth="359.512" horizDistance="52.12" distanceType="measured" azimuthType="measured" purpose="traverse" equipmentUsed="theodolite EDM" />
    <ReducedObservation name="5" setupID="IS-71-IS185989" targetSetupID="IS-72-IS185989" azimuth="359.512" horizDistance="24.574" distanceType="measured" azimuthType="measured" purpose="traverse" equipmentUsed="theodolite EDM" />
    </ObservationGroup>
    </Survey>
    <CoordinateSystem datum="OfPlan" desc="Vide IS185958" />
    </LandXML>

LandXML structure
=================

LandXML use a schema which specifies how to formally describe the elements of 
the document. The schema currently used is version 1.2.

Tags and attributs
------------------

+------------------+--------------------+------------------+--------------------------+
|       Tag        |      Attribut      |    Parent tag    | :class:`formats.Feature` |
+==================+====================+==================+==========================+
| Units            |                    |                  |                          |
+------------------+--------------------+------------------+--------------------------+
| Metric           |                    | Units            |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | linearUnit         |                  | dist_unit                |
+------------------+--------------------+------------------+--------------------------+
|                  | angularUnit        |                  | angle_unit               |
+------------------+--------------------+------------------+--------------------------+
| Imperial*        |                    | Units            |                          |
+------------------+--------------------+------------------+--------------------------+
| Survey           |                    |                  |                          |
+------------------+--------------------+------------------+--------------------------+
| SurveyHeader*    |                    | Survey           |                          |
+------------------+--------------------+------------------+--------------------------+
| Equipment*       |                    | Survey           |                          |
+------------------+--------------------+------------------+--------------------------+
| CgPoints         |                    | Survey           | "PT" in feature          |
+------------------+--------------------+------------------+--------------------------+
| CgPoint          |                    | CgPoints         | :class:`formats.Point`   |
+------------------+--------------------+------------------+--------------------------+
|                  | name               | CgPoints         | point_name               |
+------------------+--------------------+------------------+--------------------------+
| Feature          |                    | CgPoint          |                          |
+------------------+--------------------+------------------+--------------------------+
| Property         |                    | Feature          |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | values             |                  | attrib                   |
+------------------+--------------------+------------------+--------------------------+
| InstrumentSetup  |                    | Survey           | "ST" in feature          |
+------------------+--------------------+------------------+--------------------------+
|                  | id                 |                  | station_id               |
+------------------+--------------------+------------------+--------------------------+
|                  | stationName        |                  | point_name               |
+------------------+--------------------+------------------+--------------------------+
|                  | instrumentHeight   |                  | ih                       |
+------------------+--------------------+------------------+--------------------------+
|                  | orientationAzimuth |                  | hz0                      |
+------------------+--------------------+------------------+--------------------------+
|                  | circleAzimuth      |                  | hz0                      |
+------------------+--------------------+------------------+--------------------------+
| Feature          |                    | InstrumentSetup  |                          |
+------------------+--------------------+------------------+--------------------------+
| Property         |                    | Feature          |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | values             |                  | attrib                   |
+------------------+--------------------+------------------+--------------------------+
| ObservationGroup |                    | Survey           |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | setupID            |                  | station_id               |
+------------------+--------------------+------------------+--------------------------+
| Backsight        |                    | ObservationGroup |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | circle             |                  | circle                   |
+------------------+--------------------+------------------+--------------------------+
|                  | setupID            |                  | "setup" + id             |
+------------------+--------------------+------------------+--------------------------+
| BacksightPoint   |                    | ObservationGroup |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | name               |                  |                          |
+------------------+--------------------+------------------+--------------------------+
| RawObservation   |                    | ObservationGroup | "PO" in feature          |
+------------------+--------------------+------------------+--------------------------+
|                  | setupID            |                  | station_id               |
+------------------+--------------------+------------------+--------------------------+
|                  | azimuth            |                  | azimuth                  |
+------------------+--------------------+------------------+--------------------------+
|                  | horizAngle         |                  | angle                    |
+------------------+--------------------+------------------+--------------------------+
|                  | zenithAngle        |                  | z_angle                  |
+------------------+--------------------+------------------+--------------------------+
|                  | slopeDistance      |                  | dist                     |
+------------------+--------------------+------------------+--------------------------+
|                  | horizDistance      |                  | dist                     |
+------------------+--------------------+------------------+--------------------------+
|                  | targetHeight       |                  | th                       |
+------------------+--------------------+------------------+--------------------------+
| TargetPoint      |                    | RawObservation   | :class:`formats.Point`   |
+------------------+--------------------+------------------+--------------------------+
|                  | desc               |                  | point_name               |
+------------------+--------------------+------------------+--------------------------+
|                  | name               |                  | point_name               |
+------------------+--------------------+------------------+--------------------------+
| Feature          |                    | RawObservation   |                          |
+------------------+--------------------+------------------+--------------------------+
| Property         |                    | Feature          |                          |
+------------------+--------------------+------------------+--------------------------+
|                  | values             |                  | attrib                   |
+------------------+--------------------+------------------+--------------------------+

\* Not implemented

Annotations
-----------

Units :
    All angular and direction values default to radians unless otherwise noted.
    Angular values, expressed in the specified Units.angleUnit are measured 
    counter-clockwise from east=0. Horizontal directions, expressed in the specified 
    Units.directionUnit are measured counter-clockwise from 0 degrees = north.

CgPoints :
    A collection of COGO points. (Cg = COGO = Cordinate Geometry).

InstrumentSetup :
    The Instrument setup location is defined by either a coordinate text value 
    ("north east" or "north east elev") or a CgPoint number reference "pntRef" 
    attribute.

ObservationGroup :
    All observations to the same point in a group should be averaged together 
    (they have consistant orientation).

TargetPoint :
    Represents a 2D or 3D location for the target.
    It is defined by either a coordinate text value ("north east" or "north east 
    elev") or a CgPoint number reference "pntRef" attribute.



Known limitations
=================

Support for all tags is still incomplete, here is a list of **TODO**:
  * add all missing tags
  * add the possibility to customize code

.. seealso::

  `Schema 1.2 for LandXML  <http://www.landxml.org/schema/LandXML-1.2/documentation/LandXML-1.2Doc.html>`_ |br|
