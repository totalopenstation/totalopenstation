# -*- coding: utf-8 -*-
# filename: formats/zeiss_rec_500.py
# Copyright 2008-2011 Stefano Costa <steko@iosa.it>
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

from . import Parser, Point


class FormatParser(Parser):

    def __init__(self, data):
        Parser.__init__(self, data, swapXY=True)

    def is_point(self, line):
        try:
            tokens = {
                'sequence': line[0:7],
                'pid': line[8:27],
                'text': line[27:32],
                'X_str': line[36],
                'x': line[38:50],
                'Y_str': line[51],
                'y': line[53:66],
                'Z_str': line[67],
                'z': line[69:80],
                }
            int(tokens['sequence'])
            int(tokens['pid'])
            float(tokens['x'])
            float(tokens['y'])
            float(tokens['z'])
            assert tokens['X_str'] == 'X'
            assert tokens['Y_str'] == 'Y'
            assert tokens['Z_str'] == 'Z'
        except (ValueError, IndexError, AssertionError):
            is_point = False
        else:
            is_point = True
        return is_point

    def get_point(self, line):
        '''Gets a point from a line retrieving basic data.'''

        tokens = {
            'pid': line[8:27].strip(),   # the result is more elegant than
            'text': line[27:32].strip(), # the code (Heisenberg rocks!)
            'x': line[38:50].strip(),
            'y': line[53:66].strip(),
            'z': line[69:80].strip(),
            }

        point_id = int(tokens['pid'])
        text = str(tokens['text'])

        # note that for now we keep floats into strings to avoid approximation
        # problems, provided that for writing DXF a string is sufficient.
        # FIXME before introducing new output formats.
        # We could use string formatting operations to store data as floats
        # and convert them to strings with the needed precision on the fly.

        x = str(tokens['x'])
        y = str(tokens['y'])
        z = str(tokens['z'])
        # Even here it would have been better not giving x and y the
        # wrong values(the inverted ones)but directly the right ones!

        p = Point(point_id, y, x, z, text)

        # Here it's always True so it's not worthy making the machine
        # evaluating the condition.

        #if self.swapXY is True:
            #p = Point(point_id, y, x, z, text)
        #else:
            #p = Point(point_id, x, y, z, text)

        return p
