#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_dat.py
# Copyright 2008-2010 Stefano Costa <steko@iosa.it>
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


def to_dat(e):
    if e[4].endswith("R"):
        string = "%s %s %s %s\r\n" % (e[0], e[0], e[1], e[2])
        return string
    else:
        return ''


class OutputFormat:

    """
    Exports points data in DAT format suitable for use with Archis.

    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data):
        self.data = data

    def process(self):
        lines = [to_dat(e) for e in self.data]
        output = "".join(lines)
        return output
