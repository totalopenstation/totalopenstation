=======================================
:mod:`leica_tcr_1205` -- Leica TCR 1205
=======================================


.. moduleauthor:: Stefano Costa <steko@iosa.it>
.. moduleauthor:: Luca Bianconi <luxetluc@yahoo.it>

Description
-----------

This is a quite recent total station. Data were provided by Joseph Reeves of
Oxford Archaeology.

Connection
----------

:Baudrate: higher than 19200
:Bytesize: 8
:StopBits: 1
:Parity: None

Data format
-----------

The data format is ASCII, quite simple.

The only thing to note is that data dumps contain both relative and absolute
measures.

:ref:`if_leica_tcr_1205`


=====================================
:mod:`nikon_npl_350` -- Nikon NPL-350
=====================================


.. moduleauthor:: Stefano Costa <steko@iosa.it>

Description
-----------

Connection
----------

Even the brute method ``cat /dev/ttyS0 > file`` creates an ASCII file without
any problem, so probably the default parameters for the serial port are OK.

:Baudrate: higher than 19200
:Bytesize: 8
:StopBits: 1
:Parity: None

Data format
-----------

The data format is in ASCII format.

:ref:`if_nikon_raw`


=======================================
:mod:`trimble` -- Trimble
=======================================


.. moduleauthor:: Stefano Costa <steko@iosa.it>

Description
-----------

Connection
----------

:Baudrate: 9600
:Bytesize: 8
:StopBits: 1
:Parity: None

Data format
-----------

The data format is ASCII, quite simple.

:ref:`if_trimble_are`


=======================================
:mod:`zeiss_elta_r55` -- Zeiss Elta R55
=======================================


.. moduleauthor:: Stefano Costa <steko@iosa.it>


Description
-----------

This is a quite old device, in use at the University of Siena. The
first steps in TOPS development were achieved with it.


Connection
----------

The hardware interface consists of a serial RS232 cable, that works also with
a common :term:`serial-USB adapter` .

:Baudrate: 9600
:Bytesize: 7
:Parity: None


Output formats
--------------

The Zeiss Elta R55 total station can output data in four different
formats, only one of which is currently supported:

- :ref:`if_zeiss_rec_500`
- Zeiss R-4
- Zeiss R-5
- Zeiss R-E
