#! /usr/bin/env python

__all__ = ["tops_csv", "tops_dxf", "tops_dat", "tops_sql", "tops_txt"]

BUILTIN_OUTPUT_FORMATS = {
    'dxf': ('tops_dxf', 'OutputFormat', 'DXF'),
    'csv': ('tops_csv', 'OutputFormat', 'CSV'),
    'sql': ('tops_sql', 'OutputFormat', 'OGC-SQL'),
    'dat': ('tops_dat', 'OutputFormat', 'DAT'),
    'txt': ('tops_txt', 'OutputFormat', 'Text'),
    }

# Conditional formats
try:
    import geojson
except ImportError:
    pass
else:
    BUILTIN_OUTPUT_FORMATS['geojson'] = ('tops_geojson', 'OutputFormat', 'GeoJSON')
