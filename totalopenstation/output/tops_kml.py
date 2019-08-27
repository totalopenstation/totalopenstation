# -*- coding: utf-8 -*-
# filename: tops_kml.py
# Copyright 2017 Stefano Costa <steko@iosa.it>

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

from fastkml import kml

from totalopenstation.formats import Point, LineString, Feature, FeatureCollection


class OutputFormat:
    '''A KML output driver, based on fastkml.

    See https://developers.google.com/kml/ for the reference documentation.'''

    def __init__(self, data):
        self.feature_collection = FeatureCollection(data)

    def process(self):
        k = kml.KML()
        ns = '{http://www.opengis.net/kml/2.2}'
        d = kml.Document(ns, 'docid', 'doc name', 'doc description')
        k.append(d)
        f = kml.Folder(ns, 'fid', 'f name', 'f description')
        d.append(f)

        for feature in self.feature_collection:
            p = kml.Placemark(ns, str(feature.id), 'name', feature.desc)
            p.geometry = feature.geometry
            f.append(p)

        return k.to_string(prettyprint=True)
