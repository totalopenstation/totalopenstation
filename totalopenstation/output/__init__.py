#! /usr/bin/env python

__all__ = ["tops_csv", "tops_dxf", "tops_dat", "tops_sql", "tops_txt", "tops_geojson"]

BUILTIN_OUTPUT_FORMATS = {
    'dxf': ('tops_dxf', 'OutputFormat', 'DXF'),
    'csv': ('tops_csv', 'OutputFormat', 'CSV'),
    'sql': ('tops_sql', 'OutputFormat', 'OGC-SQL'),
    'dat': ('tops_dat', 'OutputFormat', 'DAT'),
    'txt': ('tops_txt', 'OutputFormat', 'Text'),
    'geojson': ('tops_geojson', 'OutputFormat', 'GeoJSON'),
    }
