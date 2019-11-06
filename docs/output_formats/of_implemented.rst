..rubric:: Foreword

In this page, formats are described using labels which are:

+----------+------------------------------+
|  Label   |         Explanation          |
+==========+==============================+
| PID      | Point number or referenc     |
+----------+------------------------------+
| type     | Point type (see below)       |
+----------+------------------------------+
| angle    | Horizontal angle or azimuth  |
+----------+------------------------------+
| z_angle  | zenithal angle               |
+----------+------------------------------+
| distance | Horizontal or slope distance |
+----------+------------------------------+
| th       | Target heigh                 |
+----------+------------------------------+
| ih       | Instrument heigh             |
+----------+------------------------------+
| circle   | Angle on the circle          |
+----------+------------------------------+
| station  | Station point for reference  |
+----------+------------------------------+
| TEXT     | Some descriptive text        |
+----------+------------------------------+

Point type

+------+---------------------------------------+
| Type |              Explanation              |
+======+=======================================+
| PT   | Simple point with only coordinates    |
+------+---------------------------------------+
| ST   | Station                               |
+------+---------------------------------------+
| BS   | Backsight point                       |
+------+---------------------------------------+
| PO   | Point with polar coordinates and more |
+------+---------------------------------------+


======================
:mod:`tops_csv` -- CSV
======================

Description
-----------

This is a standard file format for spreadsheet and transfer between softwares. |br|
The file is comma separated.

Data format
-----------

Yet, this format is not parametric and values return are the following::

    PID, type, Point Name, x, y, angle, z_angle, distance, th, ih, circle, station


======================
:mod:`tops_dat` -- DAT
======================

Description
-----------

This format is used in Archis software for photorectification, photo mosaic and
photogrammetric survey.

Data format
-----------

Return format is points coordinates::

    PID, x, y, z, TEXT


======================
:mod:`tops_dxf` -- DXF
======================

Description
-----------

This format is a standard format for CAD softwares like AutoCAD, QCAD,
LibreCAD...

Data format
-----------

The format is based on the official `DXF R15 (2000) documentation
<https://www.autodesk.com/techpubs/autocad/acad2000/dxf/index.htm>`_. |br|
Layers can be separated for each point or not. |br|
This format can describe points or lines.


==============================
:mod:`tops_geojson` -- GeoJSON
==============================

Description
-----------

This format follow the GeoJSON standard
`RFC 7946 <https://tools.ietf.org/html/rfc7946>`_. |br|
Moreover, this format is the internal format used in Total Open Station. |br|
It is supported by numerous mapping and GIS software.

Data format
-----------

GeoJSON features collections.

======================
:mod:`tops_sql` -- SQL
======================

Description
-----------

This format is used by PostGIS which adds support for geographic objects to the
PostgreSQL object-relational database.|br|
`SQL Reference <http://postgis.net/docs/manual-2.5/using_postgis_dbmanagement.html>`_

Data format
-----------

Format is points coordinates::

    PID, x, y, z, TEXT


======================
:mod:`tops_txt` -- Txt
======================

Description
-----------

A simple ASCII format to export points coordinates.

Data format
-----------

Format is points coordinates::

    x, y, z
