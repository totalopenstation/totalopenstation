#! /usr/bin/env python

__all__ = ["tops_csv", "tops_dxf", "tops_dat", "tops_sql", "tops_txt", "tops_geojson"]

class Builder:

    def __init__(self, data):
        """Init method which **must** be overridden in the child class
        to have a working builder.
        
        Args:
        data (:class:`formats.Parser`): A list of :class:`formats.Feature`
        """

        self.data = data
    
    def process(self):
        """Action for building the output string.
        
        This method **must** be overridden in the child class
        to have a working builder.
        
        Process the input data (processing data).
        This is because we want to keep the generation of output separated from
        saving it to disk.

        Return:
            str: A string representing the value to output.
        """

        pass


BUILTIN_OUTPUT_FORMATS = {
    'dxf': ('tops_dxf', 'OutputFormat', 'DXF'),
    'csv': ('tops_csv', 'OutputFormat', 'CSV'),
    'sql': ('tops_sql', 'OutputFormat', 'OGC-SQL'),
    'dat': ('tops_dat', 'OutputFormat', 'DAT'),
    'txt': ('tops_txt', 'OutputFormat', 'Text'),
    'geojson': ('tops_geojson', 'OutputFormat', 'GeoJSON'),
    }
