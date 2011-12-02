Data
====

For each device, there are 2 kind of information needed:

* connection parameters for downloading correctly data from the serial port
* data model for parsing of the downloaded data

Connection parameters
---------------------

I decided to use the **pySerial** library, that works well and has a
cross-platform interface. Connection parameters are expressed as arguments
of the ``Serial`` class:

>>> zeiss = serial.Serial('/dev/ttyUSB0', baudrate=9600,
    bytesize=serial.SEVENBITS, timeout=0, parity=serial.PARITY_NONE, rtscts=1)

Things to note:

* the connection port can also be indicated with a number, that is platform
  indipendent, but I don't know if this means that the user has to enter the
  port manually
* the standard ``baudrate`` is 9600
* setting ``timeout`` = 0 makes the device not emit errors nor strange beeps
* the other options work, but I cannot explain them

Data model
----------

The main information that we should get is made by the XYZ coordinates of each
recorded point. This kind of information can probably be stored safely using
a PythonGeoInterface_ or something similar.

.. _PythonGeoInterface: http://trac.gispython.org/projects/PCL/wiki/PythonGeoInterface

Each point must also be assigned its ID, that is the same recorded on the
device.

Each session has an arbitrary origin point, that each point must reference
as an attribute to be able to patch different sessions together.

It should be noted that these coordinates do not express any geographic nor
cartographic position, and using GIS tools it's always difficult to avoid
definining a Coordinate Reference System for your data. Often WGS84 is
implicit if you don't specify one.

