.. _output_formats:

==============
Output formats
==============

Total Open Station supports a number of output formats.

As input formats, data formats can be classified into two groups:

1. "raw" data with polar coordinates and lots of information
2. processed data with cartesian coordinates

.. _implemented_of:

Implemented formats
===================

Output formats are:

.. toctree::
    :maxdepth: 1
    :glob:

    of_*

Unknown formats
===============

Unimplemented :term:`formats <output format>` can be added to
Total Open Station.

The best way to have your format included in the next version of
Total Open Station is to fill a support request in the `bug tracker`_ and attach
some sample data dumps obtained from your original software.

If you can write Python code, you can also write a module by yourself using
an existing one as a guide and the :ref:`new` directive. 
If you write a module, we will be happy to receive it and include it in the
Total Open Station source tree.

.. seealso::
    The :ref:`contributing` page to find out how to join the project and
    participate actively to the development.
