#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: output/formats.py
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

formats = {
    'DXF': 'tops_dxf',
    'CSV': 'tops_csv',
    'SQL': 'tops_sql',
    'DAT': 'tops_dat',
    'TXT': 'tops_txt'
    }

# Conditional formats
try:
    import geojson
except ImportError:
    pass
else:
    formats['GeoJSON': 'tops_geojson']

if __name__ == '__main__':
    print("List of supported output formats:\n------------------------")
    for k, v in formats.items():
        print k.ljust(10), v
    print("")
