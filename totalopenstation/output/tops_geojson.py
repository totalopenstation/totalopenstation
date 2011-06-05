# -*- coding: utf-8 -*-
# filename: tops_geojson.py
# Copyright 2009 Stefano Costa <steko@iosa.it>

# This file is part of Total Open Station.

# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.

import geojson


def output_geojson(data):
    '''A GeoJSON output driver.'''

    fs = []

    for point in data:
        pid, x, y, z, text = point
        x, y, z = [float(c) for c in x, y, z]
        p = geojson.Point([x, y, z])
        prop = dict(text=text)
        f = geojson.Feature(id=pid, geometry=p, properties=prop)
        fs.append(f)
    fc = geojson.FeatureCollection(fs)
    return geojson.dumps(fc)


class TotalOpenGEOJSON:
    '''A GeoJSON output driver.

    Depends on the geojson package http://pypi.python.org/pypi/geojson/

    FIXME This is an example of how classes are probably useless for
    coding output formats. A transition towards an eventual new
    structure could be done in 2 passages, the first being making the
    current classes empty wrappers around a function.'''

    def __init__(self, data):

        self.data = data

    def process(self):

        return output_geojson(self.data)
