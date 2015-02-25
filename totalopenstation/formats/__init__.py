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


class Point:

    def __init__(self, p_id, x, y, z, text):

        self.p_id = p_id
        self.x = x
        self.y = y
        self.z = z
        self.text = text

        self.tuplepoint = (self.p_id, self.x, self.y, self.z, self.text)

    def __str__(self):
        return 'Point(%(p_id)s, %(x)s, %(y)s, %(z)s, %(text)s)' % self.__dict__


class Parser:
    '''Parses a *single* string of raw data.

    This means that if you plan to load data from a file you have to
    pass the output of open(file).read() to this class.'''

    def __init__(self, data, swapXY=False):

        self.data = data
        self.d = self.split_points()
        self.swapXY = swapXY

        valid_lines = filter(self.is_point, self.d)
        fg_lines = map(self.get_point, valid_lines)
        self.points = [p.tuplepoint for p in fg_lines if p is not None]

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


BUILTIN_INPUT_FORMATS = {
    'carlson_rw5': ('carlson_rw5', 'FormatParser', 'Carlson RW5'),
    'leica_gsi': ('leica_gsi', 'FormatParser', 'Leica GSI'),
    'leica_tcr_705': ('leica_tcr_705', 'FormatParser', 'Leica TCR 705'),
    'leica_tcr_1205': ('leica_tcr_1205', 'FormatParser', 'Leica TCR 1205'),
    'nikon_raw_v200': ('nikon_raw_v200', 'FormatParser','Nikon RAW V2.00'),
    'sokkia_sdr33': ('sokkia_sdr33', 'FormatParser', 'Sokkia SDR33'),
    'topcon_gts': ('topcon_gts', 'FormatParser', 'Topcon GTS'),
    'trimble_are': ('trimble_are', 'FormatParser', 'Trimble AREA'),
    'zeiss_rec_500': ('zeiss_rec_500', 'FormatParser', 'Zeiss REC 500'),
    }
