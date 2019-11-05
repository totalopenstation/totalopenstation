#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_txt.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com>
# Copyright 2019 Stefano Costa <steko@iosa.it>
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


def to_txt(d):
    try:
        string = "{geom.x} {geom.y} {geom.z}\n".format(geom=d.geometry)
    except ValueError:
        string = "{geom.x} {geom.y}\n".format(geom=d.geometry)
    return string

class OutputFormat(Builder):

    """
    Exports points data in TXT (space-separated) format line by line.

    ``data`` should be an iterable of Feature objects.
    """

    def __init__(self, data):
        self.data = data

    def process(self):
        lines = [to_txt(e) for e in self.data]
        output = "".join(lines)
        return output
