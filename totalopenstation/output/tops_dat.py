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

from . import Builder


def to_dat(point):
    result = "{p.id} {p.id} {p.geometry.x} {p.geometry.y}\r\n".format(p=point)
    return result


class OutputFormat(Builder):

    """
    Exports points data in DAT format suitable for use with Archis.

    ``data`` must be an iterable containing Feature objects.
    """

    def __init__(self, data):
        self.data = data

    def process(self):
        lines = [to_dat(point) for point in self.data]
        output = "".join(lines)
        return output
