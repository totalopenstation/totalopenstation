=========================
 :mod:`leica_gsi` -- GSI
=========================

.. module:: leica_gsi
    :platform: any
    :synopsis: Read data in the GSI8 and GSI16 formats
.. moduleauthor:: Stefano Costa
.. versionadded:: 0.4

GSI is a very popular data format, used by many Leica total stations. It is
stored as ASCII text, with one line per measurement. In each line, there can
be several *blocks* of data, with a blank space as a separation.

There are two variants of GSI:

- GSI8
- GSI16

but they only differ in the size of a single *block*.

GSI is a very rich format, and it can hold both cartesian and polar coordinates
with a detailed recording of all commands executed by the device and with
explicit indication of the measurement units.

Known limitations
=================

Support for raw measurements is still incomplete, namely it lacks support for
base station points, except in some specific cases when the base point
coordinates are directly associated with each measurement.

Measurement units (both for distances and angles) are not supported yet.

Acknowledgements
================

Support for this format was added thanks to Anna Hodgkinson and Hannah Petten
at the University of Liverpool. Some details of the implementation are based
on the SurveyTools QGIS plugin developed by Stefan Ziegler.

.. seealso::

   `GSI Online for Leica TPS <http://www.leica-geosystems.com/media/new/product_solution/gsi_manual.pdf>`_ 
      Documentation for GSI from Leica.
