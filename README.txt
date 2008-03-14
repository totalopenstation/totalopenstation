====================
 Total Open Station
====================
--------------------------------------------------------------------------
A generic Python interface for downloading data from total station devices
--------------------------------------------------------------------------

Introduction
============

I started writing this program for making it easier to manage different
models of total stations, often used in the same fieldwork unit, mainly in a
GNU/Linux environment. However, I try to develop following standards, so
porting to Windows or Mac shouldn't be difficult.

Every model has its own quirks. So, I decided to use a modular structure,
that is based on an abstract interface. Each time a new model is added to
the program, you create a new instance of this base class, with all needed
data.

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

Models
======

Zeiss Elta R55
--------------

The hardware interface consists of a serial RS232 cable, that works also with
common serial-usb adapters.

>>> import serial
>>> ser = serial.Serial('/dev/ttyUSB0', \
    baudrate=9600, bytesize=serial.SEVENBITS, timeout=0, \
    parity=serial.PARITY_NONE, rtscts=1)
>>> ser.open()

At this point, you have to start the download from the device menu. When this
operation has finished, it's good practice to control if you have actually
received any data:

>>> ser.inWaiting()
648L

A non-zero result means that something has been downloaded. Good enough.

This number can be saved to a variable and passed as parameter to the
``read()`` command

>>> n = ser.inWaiting()
>>> result = ser.read(n)

The ``result`` object is a string that contains our data:

>>> print(result)
   0001 OR.COOR                                                                
   0002                   0S        X        0.000 Y         0.000 Z     0.000 
   0003                                            Om     397.0370             
   0004 POLAR                                                                  
   0005 INPUT                       th       1.500 ih        0.000             
   0006 INPUT                       th       0.000 ih        0.000 Z     0.000 
   0007                   1         X       -0.472 Y         1.576 Z     0.004 
END                                                                            

So far, we can say that the downloaded file contains this information:

* ``OR.COOR``: but I don't know if this line can take other values too
* **origin point** defined by the ``OS`` string followed by its ``X``, ``Y``,
  ``Z`` coordinates
* **orientation angle** ``Om``: are these gradiants?
* ``POLAR``: but I don't know if this line can take other values too
* ``INPUT``: are there always two ``INPUT`` lines?

  * ``th``
  * ``ih``
  * ``Z``

* points, expressed as ``N`` (starting from 1), ``X``, ``Y``, ``Z``
* ``END``: after this line no more data

Nikon NPL-350
-------------

Download is in ASCII format.

Even the brute method ``cat /dev/ttyS0 > file`` creates an ASCII file without any
problem, so probably the default parameters for the serial port are OK.


Other models
------------

At the moment I haven't had access to any other model. The best would be to
create a standard procedure to enable anyone to get the right parameters for
their model executing a simple test and sending us their results.

This way we can start also giving general information about makers that can
be helpful when testing.

This information and other about specific models could be inserted in a wiki
and organized in a database to be distributed along with the program.

