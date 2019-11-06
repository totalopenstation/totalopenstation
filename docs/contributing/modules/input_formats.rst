=============
Input Formats
=============

This module is used as a base for parsing input files.

The main class is :class:`formats.Parser`.

Each input format module has a child class named *FormatParser(Parser)*.

Classes
=======

.. automodule:: formats
   :members:
   :member-order: bysource
   :undoc-members:
   :show-inheritance:

Constants
=========

* .. data:: BUILTIN_INPUT_FORMATS

        Dictionnary that holds all input formats available in Total Open Station.

        Form of the dictionnary :
        
        { |br|
        'parser_name': ('module_parser_name', 'FormatParser', 'Parser Name'), |br|
        }

* .. data:: UNITS_CIRCLE

        Dictionnary that holds angle corresponding to the complet ride of a
        circle per units.

        Form of the dictionnary :

            { |br|
            'name': numeric value of complet ride, |br|
            }

* .. data:: UNKNOWN_STATION

        :class:`formats.Point` that holds arbitary coordinates of an unknown station. |br|
        These coordinates are not egals to zero to avoid negativ coordinates during
        computation.

        Point(10000, 10000, 100)

* .. data:: UNKNOWN_POINT

        :class:`formats.Point` that holds arbitary coordinates of an unknown point. |br|
        These coordinates are negatives to be able to check them during computation.

        Point(-1, -1, -1)

* .. data:: COORDINATE_ORDER

        tuple that holds possible coordinates order in some input formats.

        ('NEZ', 'ENZ')


