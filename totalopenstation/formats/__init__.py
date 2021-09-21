# -*- coding: utf-8 -*-
# filename: formats/__init__.py
# Copyright 2008-2010 Stefano Costa <steko@iosa.it>
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2015-2016 Damien Gaignon <damien.gaignon@gmail.com>

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

import logging

from pygeoif import geometry as g
from math import pi


logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

class Point(g.Point):
    pass


class LineString(g.LineString):
    pass


class Feature(g.Feature):
    '''A GeoJSON-like Feature object.'''

    def __init__(self, geom, desc, id=None, **properties):
        g.Feature.__init__(self, geom, properties, feature_id=id)
        self.properties['desc'] = desc

    @g.Feature.geometry.setter
    def geometry(self, value):
        '''Set the geometry attribute.

        By default, geometry property return the geometry value.
        '''

        self._geometry = value

    @property
    def desc(self):
        '''Return the desc property
        '''

        return self.properties['desc']

    @property
    def point_name(self):
        '''Return the point_name property
        '''

        return self.properties['point_name']


class FeatureCollection(g.FeatureCollection):
    pass


class Parser:
    '''Parses a *single* string of raw data.

    This means that if you plan to load data from a file you have to
    pass the output of open(file).read() to this class.

    Args:
        data (str): A string representing the file to be parsed.
            
    Attributes:
        data (str): A string representing the file to be parsed **could**
            be overridden by the init method.
    '''

    def __init__(self, data):
        """Init method which **should** be overridden in the child class
        to have a working parser."""

        self.data = data

    def is_point(self, line):
        """Action for finding which parts of the source file are points.

        This method **must** be overridden in the child class
        to have a working parser.
        
        Returns:
            A boolean
        """

        pass

    def get_point(self, line):
        """Action for getting points from source file.

        This method **must** be overridden in the child class
        to have a working parser.
        
        Returns:
            A :class:`formats.Feature` object."""

        pass

    def split_points(self):
        """Action for splitting points.

        Defaults to ``splitlines()`` because most formats have one
        point per line.

        Override this method if the format is different."""

        return self.data.splitlines()

    def build_linestring(self):
        '''Join all Point objects into a LineString.
        
        Returns:
            A :class:`formats.LineString` object.
        '''

        return LineString([f.geometry for f in self.points])

    @property
    def points(self):
        """Action for parsing a source file and for finding points.

        This method **could** be overridden in the child class
        to have a working parser.
        
        Returns:
            A list of GeoJSON-like Feature object representing points coordinates.
        """


        self.d = self.split_points()

        valid_lines = filter(self.is_point, self.d)
        fg_lines = map(self.get_point, valid_lines)

        return [p for p in fg_lines if p is not None]

    @property
    def raw_line(self):
        """Action for parsing a source file and for retrieving raw data.

        This method **must** be overridden in the child class
        to have a working parser.
        
        Returns:
            A list of GeoJSON-like Feature object representing
            representing raw data i.e. polar coordinates and other
            informations.
        """

        pass


def check_coordorder(coordorder):
    '''Check if coordinates order is valid.

    Args:
        coordorder (str): A string representing the type of coordinates i.e.
                NEZ or ENZ.
    '''

    if any((coordorder == v for v in COORDINATE_ORDER)):
        return coordorder
    else:
        logger.info('Invalid coordinate order')

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

UNITS_CIRCLE = {
    'dms': 360,
    'deg': 360,
    'gon': 400,
    'mil': 6400,
    'rad': 2 * pi,
    }

UNKNOWN_STATION = Point(10000, 10000, 100)
UNKNOWN_POINT = Point(-1, -1, -1)

COORDINATE_ORDER = ('NEZ', 'ENZ')
