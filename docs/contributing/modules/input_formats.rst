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

        Dictionnary that holds all input formats available in |tops|.
        
        { |br|
        'carlson_rw5': ('carlson_rw5', 'FormatParser', 'Carlson RW5'), |br|
        'leica_gsi': ('leica_gsi', 'FormatParser', 'Leica GSI'), |br|
        'leica_tcr_705': ('leica_tcr_705', 'FormatParser', 'Leica TCR 705'), |br|
        'leica_tcr_1205': ('leica_tcr_1205', 'FormatParser', 'Leica TCR 1205'), |br|
        'nikon_raw_v200': ('nikon_raw_v200', 'FormatParser','Nikon RAW V2.00'), |br|
        'sokkia_sdr33': ('sokkia_sdr33', 'FormatParser', 'Sokkia SDR33'), |br|
        'topcon_gts': ('topcon_gts', 'FormatParser', 'Topcon GTS'), |br|
        'trimble_are': ('trimble_are', 'FormatParser', 'Trimble AREA'), |br|
        'zeiss_r5': ('zeiss_r5', 'FormatParser', 'Zeiss R5'), |br|
        'zeiss_rec_500': ('zeiss_rec_500', 'FormatParser', 'Zeiss REC 500'), |br|
        }

* .. data:: UNITS_CIRCLE

        Dictionnary that holds angle corresponding to the complet ride of a
        circle per units.

            { |br|
            'dms': 360, |br|
            'deg': 360, |br|
            'gon': 400, |br|
            'mil': 6400, |br|
            'rad': 2 * pi, |br|
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


