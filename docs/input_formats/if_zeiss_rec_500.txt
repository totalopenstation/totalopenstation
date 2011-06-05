.. _if_zeiss_rec_500:

========================================
 :mod:`zeiss_rec_500` -- Zeiss REC 500
========================================

.. module:: zeiss_rec_500
    :platform: any
    :synopsis: Read data in the Zeiss REC 500 format
.. moduleauthor:: Stefano Costa


This was the first format supported by Total Open Station. For
historical reasons, its documentation is far more extended than those
of other formats. The step by step procedure is useful for anyone who
wants to hack on TOPS itself.

Step-by-step download procedure
-------------------------------

At the time I was doing the first tests, I found it useful to collect
all steps. The program goes through them automatically::

  >>> import serial
  >>> ser = serial.Serial('/dev/ttyUSB0', \
      baudrate=9600, bytesize=serial.SEVENBITS, timeout=0, \
      parity=serial.PARITY_NONE, rtscts=1)
  >>> ser.open()

At this point, you have to start the download from the device
menu. When this operation has finished, it's good practice to control
if you have actually received any data::

  >>> ser.inWaiting()
  648L

A non-zero result means that something has been downloaded. Good enough.

This number can be saved to a variable and passed as parameter to the
``read()`` command::

  >>> n = ser.inWaiting()
  >>> result = ser.read(n)

The ``result`` object is a string that contains our data::

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
