.. _LandXML website: http://www.landxml.org/

.. _of_landxml:

==============================
:mod:`tops_landxml` -- LandXML
==============================

.. moduleauthor:: Damien Gaignon
.. versionadded:: 0.6

Description
-----------

LandXML is committed to providing an non-proprietary data standard (LandXML),
driven by an consortium of partners for the inter-operability of data utilized
within the Land Development industry.

The official documentation about the format is provided on the `LandXML website`_.

LandXML is a specialized XML (eXtensible Mark-up Language) data file format
containing civil engineering and survey measurement data commonly used in the
Land Development and Transportation Industries.

LandXML structure
-----------------

LandXML use a schema which specifies how to formally describe the elements of 
the document. The schema currently used is version 1.2.

Units tag
_________

Currently, the header of the XML file will always be::

    <?xml version="1.0"?>
    <LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.landxml.org/schema/LandXML-1.2 http://www.landxml.org/schema/LandXML-1.1/LandXML-1.1.xsd" date="" time="" version="1.1">
        <Units>
            <Metric areaUnit="squareMeter" linearUnit="meter" volumeUnit="cubicMeter" temperatureUnit="celsius" pressureUnit="milliBars" angularUnit="grads" directionUnit="grads"></Metric>
        </Units>
        <Project name="Template"></Project>
        <Application name="TotalOpen Station" desc="TOPS" manufacturer="" version="" manufacturerURL="http://tops.iosa.it/" timeStamp=""></Application>
    </LandXML>

Metric is choosed as the default unit system.
If one need Imperial, ask for it in the `bug tracker`_.

Tags and attributs
__________________


+------------------+---------------------+----------------------------+------------------+
|       Tag        |      Attribut       |           Value            |    Parent tag    |
+==================+=====================+============================+==================+
| Survey           |                     |                            |                  |
+------------------+---------------------+----------------------------+------------------+
| SurveyHeader     |                     |                            | Survey           |
+------------------+---------------------+----------------------------+------------------+
|                  | name                | "from TOPS"                | Survey           |
+------------------+---------------------+----------------------------+------------------+
| Equipment        |                     |                            | Survey           |
+------------------+---------------------+----------------------------+------------------+
| CgPoints         |                     |                            | Survey           |
+------------------+---------------------+----------------------------+------------------+
| CgPoint          |                     | x y [z]                    | CgPoints         |
+------------------+---------------------+----------------------------+------------------+
|                  | name                | point_name                 |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | pntRef              | pid                        |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | featureRef          | "feature" + point_name     |                  |
+------------------+---------------------+----------------------------+------------------+
| Feature          |                     |                            | CgPoint          |
+------------------+---------------------+----------------------------+------------------+
|                  | name                | "feature" + point_name     | CgPoint          |
+------------------+---------------------+----------------------------+------------------+
| Property         |                     |                            | Feature          |
+------------------+---------------------+----------------------------+------------------+
|                  | "attrib" + index    | attrib[index]              |                  |
+------------------+---------------------+----------------------------+------------------+
| InstrumentSetup  |                     |                            | Survey           |
+------------------+---------------------+----------------------------+------------------+
|                  | id                  | "setup" + id               |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | stationName         | point_name                 |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | instrumentHeight    | ih                         |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | orientationAzimuth  | hz0                        |                  |
+------------------+---------------------+----------------------------+------------------+
| Feature          |                     |                            | InstrumentSetup  |
+------------------+---------------------+----------------------------+------------------+
|                  | name                | "feature" + point_name     | CgPoint          |
+------------------+---------------------+----------------------------+------------------+
| Property         |                     |                            | Feature          |
+------------------+---------------------+----------------------------+------------------+
|                  | "attrib" + index    | attrib[index]              |                  |
+------------------+---------------------+----------------------------+------------------+
| InstrumentPoint  |                     | instru_x instru_y instru_z | InstrumentSetup  |
+------------------+---------------------+----------------------------+------------------+
|                  | pntRef              | pid                        |                  |
+------------------+---------------------+----------------------------+------------------+
| ObservationGroup |                     |                            | Survey           |
+------------------+---------------------+----------------------------+------------------+
|                  | id                  | "o" + id                   |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | setupID             | "setup" + id               |                  |
+------------------+---------------------+----------------------------+------------------+
| Backsight        |                     |                            | ObservationGroup |
+------------------+---------------------+----------------------------+------------------+
|                  | circle              | circle                     |                  |
+------------------+---------------------+----------------------------+------------------+
| BacksightPoint   |                     | back_x back_y back_z       | Backsight        |
+------------------+---------------------+----------------------------+------------------+
|                  | name                | back_name                  |                  |
+------------------+---------------------+----------------------------+------------------+
| RawObservation   |                     |                            | ObservationGroup |
+------------------+---------------------+----------------------------+------------------+
|                  | setupID*            | "setup" + id               |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | azimuth             | azimuth                    |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | horizAngle          | angle                      |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | zenithAngle         | z_angle                    |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | slopeDistance       | dist                       |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | horizDistance       | dist                       |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | targetHeight        | th                         |                  |
+------------------+---------------------+----------------------------+------------------+
| TargetPoint      |                     | x y [z]                    | RawObservation   |
+------------------+---------------------+----------------------------+------------------+
|                  | desc                | point_name                 |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | pntRef              | pid                        |                  |
+------------------+---------------------+----------------------------+------------------+
| Feature          |                     |                            | RawObservation   |
+------------------+---------------------+----------------------------+------------------+
| Property         |                     |                            | Feature          |
+------------------+---------------------+----------------------------+------------------+
|                  | instrumentHeight    | ih                         |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | edmAccuracyppm      | ppm                        |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | edmAccuracyConstant | prism_constant             |                  |
+------------------+---------------------+----------------------------+------------------+
|                  | "attrib" + index    | attrib[index]              |                  |
+------------------+---------------------+----------------------------+------------------+

/* Not implemented

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
