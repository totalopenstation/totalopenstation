# -*- coding: utf-8 -*-
# filename: formats/leica_tcr_705.py
# Copyright 2009-2010 Stefano Costa <steko@iosa.it>
# Copyright 2009-2010 Luca Bianconi <luxetluc@yahoo.it>

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

    def is_point(self, line):

        tokens = line.split(",")
        is_point = False

        try:
            float(tokens[1])
            float(tokens[2])
            float(tokens[3])
        except (ValueError, IndexError):
            is_point = False
        else:
            is_point = True
            x, y, z = tokens[1:4]

            # not so clear why there are such points recorded
            if x == '1.00' and y == '1.00' and z == '1.00':
                is_point = False

        return is_point

    def get_point(self, line):

        tokens = line.split(",")

        if len(tokens) > 4:
            text = str(tokens[4])
        else:
            text = ""

        p = Point(str(tokens[0]),
                  float(tokens[1]),
                  float(tokens[2]),
                  float(tokens[3]),
                  text)

        return p
