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

Trimble CSV
-----------

.. versionadded:: 0.7

This module contains also a variant CSV output with the same data columns,
but in a different order, Trimble CSV (used for LandSurveyCodesImport QGIS plugin)::

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

.. versionchanged:: 0.7

The DXF output now uses the `ezdxf <https://ezdxf.mozman.at/>`_ library for
robust DXF generation. Output uses the R12 format for maximum compatibility
with CAD software.

Data format
-----------

The output includes the following DXF entities:

- **Point** entities for survey points
- **Text** entities for point ID and elevation labels
- **Polyline** entities for LineString geometries

Layer organization:

- When ``separate_layers`` is enabled (default), points are organized into
  layers based on their description, with sub-layers for points, Z coordinates,
  and labels (e.g. ``WALL_POINTS``, ``WALL_Z_COORDS``, ``WALL_LABELS``)
- Each description group is assigned a distinct color


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
