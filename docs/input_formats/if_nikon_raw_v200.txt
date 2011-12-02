========================
 Nikon RAW format V2.00
========================

:author: Stefano Costa

This format contains polar data. It is the first polar format
supported by Total Open Station.

Data are basically comma-separated values, but each row can have a
different format and number of fields. Recorded points are in rows
that start with the ``SS`` string, while fixed base points start with
the ``ST`` string.

.. literalinclude:: ../../sample_data/nikon_raw_v200.tops

Acknowledgements
================

Support for this format was added thanks to Cynthia Mascione,
Università di Siena.

