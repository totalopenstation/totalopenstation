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
    
    { |br|
    'leica_tcr_1205': ('leica_tcr_1205', 'ModelConnector', 'Leica TCR 1205'), |br|
    'zeiss_elta_r55': ('zeiss_elta_r55', 'ModelConnector', 'Zeiss Elta R55'), |br|
    'nikon_npl_350': ('nikon_npl_350', 'ModelConnector','Nikon NPL 350'), |br|
    'leica_tcr_705': ('leica_tcr_705', 'ModelConnector', 'Leica TCR 705'), |br|
    'trimble': ('trimble', 'ModelConnector', 'Trimble'), |br|
    'custom': ('custom', 'CustomConnector', 'Custom/Unknown'), |br|
    }
