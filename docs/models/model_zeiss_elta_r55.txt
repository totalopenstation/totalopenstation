=========================================
 :mod:`zeiss_elta_r55` -- Zeiss Elta R55
=========================================

.. module:: zeiss_elta_r55
    :platform: Unix, Windows
    :synopsis: Get data from the Zeiss Elta R55 total station.

.. moduleauthor:: Stefano Costa <steko@iosa.it>


Description
===========

This is a quite old device, in use at the University of Siena. The
first steps in TOPS development were achieved with it.


Connection
==========

:Baudrate: 9600
:Bytesize: 7
:Parity: None


Output formats
==============

The Zeiss Elta R55 total station can output data in four different
formats, only one of which is currently supported:

- :ref:`if_zeiss_rec_500`
- Zeiss R-4
- Zeiss R-5
- Zeiss R-E


Other notes
===========

The hardware interface consists of a serial RS232 cable, that works also with
a common :term:`serial-USB adapter` .
