# -*- coding: utf-8 -*-
# filename: formats/__init__.py
# Copyright 2008-2010 Stefano Costa <steko@iosa.it>
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>

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

from pygeoif import geometry as g


class Point(g.Point):
    pass


class LineString(g.LineString):
    pass


class Feature(g.Feature):
    '''A GeoJSON-like Feature object.'''

    def __init__(self, geom, desc, id=None, **properties):
        g.Feature.__init__(self, geom, properties, feature_id=id)
        self.properties['desc'] = desc

    @property
    def desc(self):
        return self.properties['desc']


class FeatureCollection(g.FeatureCollection):
    pass


class Parser:
    '''Parses a *single* string of raw data.

    This means that if you plan to load data from a file you have to
    pass the output of open(file).read() to this class.'''

    def __init__(self, data):

        self.data = data
        self.d = self.split_points()

        valid_lines = filter(self.is_point, self.d)
        fg_lines = map(self.get_point, valid_lines)
        self.points = [p for p in fg_lines if p is not None]

    def is_point(self, point):
        """Action for finding which parts of the source file are points.

        This method **must** be overridden in the child class
        to have a working parser."""

        pass

    def get_point(self, point):
        """Action for getting points from source file.

        This method **must** be overridden in the child class
        to have a working parser."""

        pass

    def split_points(self):
        """Action for splitting points.

        Defaults to ``splitlines()`` because most formats have one
        point per line.

        Override this method if the format is different."""

        return self.data.splitlines()

    def build_linestring(self):
        '''Join all Point objects into a LineString.'''

        return LineString(map(lambda f: f.geometry, self.points))

    def raw_line(self):
        pass


BUILTIN_INPUT_FORMATS = {
    'carlson_rw5': ('carlson_rw5', 'FormatParser', 'Carlson RW5'),
    'leica_gsi': ('leica_gsi', 'FormatParser', 'Leica GSI'),
    'leica_tcr_705': ('leica_tcr_705', 'FormatParser', 'Leica TCR 705'),
    'leica_tcr_1205': ('leica_tcr_1205', 'FormatParser', 'Leica TCR 1205'),
    'nikon_raw_v200': ('nikon_raw_v200', 'FormatParser','Nikon RAW V2.00'),
    'sokkia_sdr33': ('sokkia_sdr33', 'FormatParser', 'Sokkia SDR33'),
    'topcon_gts': ('topcon_gts', 'FormatParser', 'Topcon GTS'),
    'trimble_are': ('trimble_are', 'FormatParser', 'Trimble AREA'),
    'zeiss_r5': ('zeiss_r5', 'FormatParser', 'Zeiss R5'),
    'zeiss_rec_500': ('zeiss_rec_500', 'FormatParser', 'Zeiss REC 500'),
    }
