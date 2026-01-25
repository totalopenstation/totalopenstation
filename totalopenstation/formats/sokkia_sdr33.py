# -*- coding: utf-8 -*-
# filename: formats/sokkia_sdr33.py
# Copyright 2014 Stefano Costa <steko@iosa.it>
# Copyright 2021 Enzo Cocca <enzo.ccc@gmail.com>

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

from . import Feature, Parser, Point


class FormatParser(Parser):

    def is_point(self, line):
        # TP records are points, but exclude record type 07
        if line[2:4] == 'TP' and line[0:2] != '07':
            return True
        else:
            return False

    def get_point(self, line):
        # Handle id as string, strip leading zeros
        id_str = line[12:20].strip().lstrip('0')
        try:
            id = int(id_str) if id_str else 0
        except ValueError:
            id = id_str

        y = float(line[20:32])  # Northing
        x = float(line[32:48])  # Easting
        z = float(line[48:63])  # Elevation

        if line[0:2] == '02':   # Base point
            desc = line[78:86].strip()
        if line[0:2] == '08':   # Measurement
            # Extended desc field to include full description
            desc = line[63:-1].strip()

        point = Point(x, y, z)
        feature = Feature(point, desc=desc, id=id)
        return feature
