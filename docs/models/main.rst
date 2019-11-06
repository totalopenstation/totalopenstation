.. _models:

======
Models
======

Total Open Station handle the retrieving of data from stations by serial link.
Parameters of connection for some models are directly implemented in Total Open Station.

Other models could be linked using the connect window (GUI only).

.. _implemented_models:

Implemented models
==================

Those following models have there connection tested and data are retrieved correctly.

.. toctree::
   :maxdepth: 1
   :glob:

   model_implemented

Other models
============

A connect window is available in the GUI to be able to set parameters and retrieve
data from non implemented models.

Unimplemented :term:`models <model>` can be integrated to Total Open Station.

The best way to have your model included in the next version of
Total Open Station is to fill a issue in the `bug tracker`_ and attach
the values obtained following the `Getting sample data`_ guide.

If you can write Python code, you can also write a module by yourself using
the existing ones as a guide and submit a `pull request`_.
If you write a module, we will be happy to receive it and include it in the Total Open Station source tree.

.. _getting_sample_data:

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

To do this, you can just use the main Total Open Station executable.


.. warning::

   Remember: Total Open Station has no wizard, and you have to tune the
   serial port options using your prior knowledge of your total
   station (e.g. read the manual that came with it, look at other
   programs' options).

.. seealso::
    The :ref:`contributing` page to find out how to join the project and
    participate actively to the development.
