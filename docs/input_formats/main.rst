.. _input_formats:

=============
Input formats
=============

Total Open Station supports a number of input data formats, which
are implemented separately from the device handling machinery
(i.e. downloading data from your total station, see :ref:`models`).
This is because one device can output more than one format, and at
the same time the same format can be used by more than one device
(particularly this is the case for different models by the same manufacturer).

Generally speaking, data formats can be classified into two large
groups:

1. “raw” field data with polar coordinates
2. processed data, with XY(Z) cartesian coordinates

The latter are far more easy to process, because they don't require
any computing of measurements.

XYZ formats
===========

These formats were the first kind of survey data format supported by
Total Open Station.

Cartesian coordinates just need to be extracted from ASCII data.

.. _implemented_if:

Implemented formats
===================

Formats known are :

.. toctree::
   :maxdepth: 1
   :glob:

   if_*

Other formats
=============

The following is an other known format but not implemented.

.. toctree::
   :maxdepth: 1
   :glob:

   tds


Unknown formats
===============

Unimplemented :term:`formats <input format>` can be added to
Total Open Station.

The best way to have your format included in the next version of
Total Open Station is to fill a support request in the `bug tracker`_ and attach
some sample data dumps obtained following :ref:`getting_sample_data`.

If you can write Python code, you can also write a module by yourself using
an existing one as a guide and the :ref:`new` directive.
If you write a module, we will be happy to receive it and include it in the
Total Open Station source tree.

.. seealso::
    The :ref:`contributing` page to find out how to join the project and
    participate actively to the development.
