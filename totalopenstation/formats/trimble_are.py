# -*- coding: utf-8 -*-
# filename: formats/trimble_are.py
# Copyright 2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2009 Stefano Costa <steko@iosa.it>
# Copyright 2009 Alessandro Bezzi <alessandro.bezzi@arc-team.com>
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

    def has_record_separator(self):
        """Check if the data uses '0=' as record separator.

        Returns:
            bool: True if '0=' is present in the data.
        """
        return "0=" in self.data

    def is_point(self, line):
        is_point = False
        if "5=" in line and "4=" in line and "37=" in line and "38=" in line and "39=" in line:
            is_point = True
        return is_point

    def get_point(self, chunk):
        tokens = {}
        rows = chunk.splitlines()

        for i in rows:
            if i.startswith('5='):
                tokens['n'] = i.split('=')[1]
            if i.startswith('4='):
                tokens['p'] = i.split('=')[1]
            if i.startswith('37='):
                tokens['x'] = i.split('=')[1]
            if i.startswith('38='):
                tokens['y'] = i.split('=')[1]
            if i.startswith('39='):
                tokens['z'] = i.split('=')[1]

        tokens['text'] = rows[0]

        try:
            p = Point(tokens['y'],
                      tokens['x'],
                      tokens['z'])
            if self.has_record_separator():
                f = Feature(p,
                            desc=tokens['p'],
                            id=tokens['n'])
            else:
                # When no record separator, use incremental id
                f = Feature(p,
                            desc=tokens['p'],
                            id=tokens.get('n', ''))
        except KeyError:
            pass
        else:
            return f

    def split_points(self):
        """Split data into point records.

        Uses '0=' as separator if present, otherwise uses '5='.
        """
        if self.has_record_separator():
            splitted_points = self.data.split("0=")
        else:
            splitted_points = self.data.split("5=")
        return splitted_points
