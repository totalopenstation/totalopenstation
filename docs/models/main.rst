.. _models:

======
Models
======

General concepts here about models and abstract classes.

.. _implemented_models:

Implemented models
==================

.. toctree::
   :maxdepth: 1
   :glob:
   
   model_*

Getting sample data
===================

Even when your device is not listed among the supported ones, Total
Open Station can still be useful, particularly for:

1. finding the right **serial connection parameters** from an unknown
   device. You can play with the 8 options and see the results in a
   text area. Once the downloaded results look good, you can be almost
   sure that you have used the right parameters, and we can add the
   tested model parameters to the program database;
2. retrieving **sample data** from unknown models and submit them to
   allow support of those models in future releases of the program.

To do this, you can just use the main Total Open Station
executable.


.. warning::

   Remember: Total Open Station is no wizard, and you have to tune the
   serial port options using your prior knowledge of your total
   station (e.g. read the manual that came with it, look at other
   programs' options).

Other models
============

Unimplemented :term:`models <model>` can be added to TotalOpenStation.

The best way to have your model included in the next version of
TotalOpenStation is to file a support request in the bug tracker and attach
some sample data dumps obtained with the Helper application.

If you can write Python code, you can also write a module by yourself using
the existing ones as a guide. Should you write a module, we will be happy to
receive it and include it in the TotalOpenStation source tree.

.. seealso::
    The :ref:`contributing` page to find out how to join the project and
    participate actively to the development.
   