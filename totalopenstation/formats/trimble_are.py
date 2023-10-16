# -*- coding: utf-8 -*-
# filename: formats/trimble_are.py
# Copyright 2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2009 Stefano Costa <steko@iosa.it>
# Copyright 2009 Alessandro Bezzi <alessandro.bezzi@arc-team.com>

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
        is_point = False

        if "5=" and "4=" and "37=" and "38=" and "39=" in line:
            is_point = True

        return is_point
    def value(self):
        value = False
        if "0=" in self.data:
            value = True
        return value
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
            if self.value():
                p = Point(tokens['y'],
                          tokens['x'],
                          tokens['z'])
                f = Feature(p,
                            desc=tokens['p'],
                            id=tokens['n'])

            else:
                p = Point(tokens['y'],
                          tokens['x'],
                          tokens['z'])
                f = Feature(p,
                            desc=tokens['p'],
                            id=+1)
        except KeyError:
            pass
        else:
            return f
    def split_points(self):
        if self.value():
            splitted_points = self.data.split("0=")
        else:
            splitted_points = self.data.split("5=")
        return splitted_points