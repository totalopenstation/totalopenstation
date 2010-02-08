# -*- coding: utf-8 -*-
# filename: formats/nikon_raw_v200.py
# Copyright 2010 Stefano Costa <steko@iosa.it>
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

from polar import BasePoint, PolarPoint
from . import Parser

def nikon_raw_parser(data):
    '''Parses data in Nikon RAW data format V2.00.'''

    rows = data.splitlines()
    for row in rows:
        fs = row.split(',')
        if fs[0] == 'ST':
            x = fs[-3]          # FIXME NEZ coord order shouldn't be hardcoded
            y = fs[-2]
            z = fs[-1]
            bp = BasePoint(x=x, y=y, z=z, ih=0)
        if fs[0] == 'SS':
            angle = fs[4]
            z_angle = fs[5]
            dist = fs[3]
            th = fs[2]
            p = PolarPoint(dist=dist,
                           angle=angle,
                           z_angle=z_angle,
                           th=th,
                           angle_type='gon',
                           base_point=bp)
            print(p.to_cartesian())

class FormatParser:

    def __init__(self, data):
        self.rows = data.splitlines()

    def _points(self):
        points = []
        for row in rows:
            fs = row.split(',')
            if fs[0] == 'ST':
                x = fs[-3]   # FIXME NEZ coord order shouldn't be hardcoded
                y = fs[-2]
                z = fs[-1]
                bp = BasePoint(x=x, y=y, z=z, ih=0)
            if fs[0] == 'SS':
                angle = fs[4]
                z_angle = fs[5]
                dist = fs[3]
                th = fs[2]
                p = PolarPoint(dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               angle_type='gon',
                               base_point=bp)
                    points.append(p.to_point())
        return points

    points = property(_points)
