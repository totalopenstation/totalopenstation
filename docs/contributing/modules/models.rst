======
Models
======

This module is used as a base for models submodules.

The main class is :class:`models.Connector`.

Each model module has a child class named *ModelConnector(Connector)*.

Classes
=======

.. automodule:: models
   :members:
   :member-order: bysource
   :undoc-members:
   :show-inheritance:

Constants
=========

* .. data:: BUILTIN_MODELS

    Dictionnary that holds all models available in Total Open Station.

    Form of the dictionnary :
    
    { |br|
    'model_name': ('module_name', 'ModelConnector' or 'CustomConnector', 'Model Name'), |br|
    }
