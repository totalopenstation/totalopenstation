==============
Output Formats
==============

There is not yet a main module with a parent class for output formats.

By the way, the main class is :class:`output.Builder`.

Each output format module has a child class named *OutputFormat(Builder)*.

Classe
======

.. automodule:: output
   :members: Builder
   :member-order: bysource
   :undoc-members:
   :show-inheritance:


Constants
=========

.. data:: BUILTIN_OUTPUT_FORMATS

    Dictionnary that holds all output formats available in Total Open Station.

    { |br|
    'dxf': ('tops_dxf', 'OutputFormat', 'DXF'), |br|
    'csv': ('tops_csv', 'OutputFormat', 'CSV'), |br|
    'sql': ('tops_sql', 'OutputFormat', 'OGC-SQL'), |br|
    'dat': ('tops_dat', 'OutputFormat', 'DAT'), |br|
    'txt': ('tops_txt', 'OutputFormat', 'Text'), |br|
    'geojson': ('tops_geojson', 'OutputFormat', 'GeoJSON'), |br|
    }
