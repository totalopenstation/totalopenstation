.. _input_formats:

===============
 Input formats
===============

.. versionadded:: 0.2
   Total Open Station supports a number of input data formats, which
   are implemented separately from the device handling machinery
   (i.e. downloading data from your total station). This is because
   one device can output more than one format, and at the same time
   the same format can be used by more than one device (particularly
   this is the case for different models by the same manufacturer).


.. toctree::
   
   input_formats/general

.. toctree::
   :maxdepth: 1
   :glob:

   input_formats/if_*

.. toctree::

   input_formats/other
   input_formats/new
