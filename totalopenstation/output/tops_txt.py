#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_txt.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com>
# Copyright 2008,2011 Stefano Costa <steko@iosa.it>
#
# This file is part of Total Open Station.
#
# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.


def to_txt(d):
    string = "%s %s %s\n" % (d[1], d[2], d[3])
    return string

class OutputFormat:

    """
    Exports points data in TXT (comma-separated) format line by line.

    ``data`` should be an iterable (e.g. list) containing one iterable
    (e.g.  tuple) for each point. The default order is PID, x, y, z,
    TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data):
        self.data = data

    def process(self):
        lines = [to_txt(e) for e in self.data]
        output = "".join(lines)
        return output
