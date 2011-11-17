.. _faq:

================================================
 Frequently Asked Questions (and some answers!)
================================================

I cannot connect to the COM port on Windows
===========================================

If you get errors like::

   SerialException: could not open port COM4: [Error 5] Access denied

try disabling and enabling again the COM port from the control
panel. Often these errors show a flip-flop behavior: opening a serial
port works fine the first time, but not the second. This is because
serial ports need to be explicitly closed by programs, otherwise they
will remain blocked.

Also, tools like Portmon_ help with troubleshooting problems
with serial ports on Windows.

.. _Portmon: http://technet.microsoft.com/en-us/sysinternals/bb896644
