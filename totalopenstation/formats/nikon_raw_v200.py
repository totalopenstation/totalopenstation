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

from . import Feature, Point
from .polar import BasePoint, PolarPoint
from totalopenstation.utils.conversion import dms_to_gon


class FormatParser:
    '''A FormatParser for Nikon RAW data format V2.00.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.'''

    def __init__(self, data):
        self.rows = data.splitlines()

    def _points(self):
        points = []
        for row in self.rows:
            fs = row.split(',')
            if fs[0] == 'CO':
                if fs[1].startswith('Coord Order:'):
                    coordorder = fs[1].split(':')[-1].strip()
                if fs[1].startswith('Angle Units:'):
                    if fs[1].endswith('Gons'):
                        angle_units = 'gon'
                    elif fs[1].endswith('DDDMMSS'):
                        angle_units = 'dms'
            if fs[0] == 'ST':
                x = fs[6]   # FIXME NEZ coord order shouldn't be hardcoded
                y = fs[7]
                z = fs[5]
                bp = BasePoint(x=x, y=y, z=z, ih=0)
                p = Point(x, y, z)
                f = Feature(p,
                            desc='ST',
                            id=fs[1])
                points.append(f)
            if fs[0] == 'SS':
                if angle_units == 'dms':
                    angle = dms_to_gon({"D": fs[4].split('.')[0],
                             "M": fs[4].split('.')[1][:2],
                             "S": fs[4].split('.')[1][2:],
                             "milliseconds": '0'})
                    z_angle = dms_to_gon({"D": fs[5].split('.')[0],
                               "M": fs[5].split('.')[1][:2],
                               "S": fs[5].split('.')[1][2:],
                               "milliseconds": '0'})
                else:
                    angle = float(fs[4])
                    z_angle = float(fs[5])
                dist = fs[3]
                th = fs[2]
                pid = fs[1]
                try:
                    text = fs[7]
                except IndexError:
                    text = fs[-1]
                p = PolarPoint(dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               base_point=bp,
                               pid=pid,
                               text=text,
                               coordorder=coordorder)
                f = Feature(p.to_point(),
                            desc=text,
                            id=pid)
                points.append(f)
        return points

    points = property(_points)
