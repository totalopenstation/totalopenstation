# -*- coding: utf-8 -*-
# filename: formats/leica_gsi.py
# Copyright 2012 Stefano Costa <steko@iosa.it>

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
from .polar import BasePoint, PolarPoint

# Distance units depend of the last digit
# 0, 6 and 8 are in mm, 1/10mm and 1/100mm
# 1 and 7 are in ft and 1/10000ft converted in m
UNITS = {"angle": {'21', '22', '25'},
         "distance": {'31', '32', '33', '81', '84', '87', '88'},
         "2": "gon", "3": "deg", "4": "dms", "5": "mil",
         "0": 1000, "1": 1000 / 3.28084, "6": 10000, "7": 10000 / 3.28084, "8": 100000}


class FormatParser(Parser):
    def is_point(self, line):

        # apparently GSI files are very "clean", and all lines contain data
        return True

    def get_point(self, line):
        '''Extract GSI data.

        Based on the "GSI ONLINE for Leica TPS" document.'''

        tokens = line.split()
        tdict = {}
        for t in tokens:
            t = t.lstrip('*')
            data = {
                'wordindex': t[0:2],
                'info': t[2:6],
                'sign': t[6],
                'data': t[7:],
            }
            tdict[data['wordindex']] = data

        try:
            pid = tdict['11']['info']
            text = tdict['11']['data'].lstrip('0')
        except KeyError:
            return None
        try:
            x = tdict['81']['sign'] + tdict['81']['data']
            y = tdict['82']['sign'] + tdict['82']['data']
            z = tdict['83']['sign'] + tdict['83']['data']
        except KeyError:
            try:
                angle_type = list(UNITS['angle'] & set(tdict.keys()))[0]
                angle_type = UNITS[tdict[angle_type]['info'][3]]
                angle = float(tdict['21']['sign'] + tdict['21']['data']) / 100000
                z_angle = float(tdict['22']['sign'] + tdict['22']['data']) / 100000
                dist_type = list(UNITS['distance'] & set(tdict.keys()))[0]
                dist_type = UNITS[tdict[dist_type]['info'][3]]
                dist = float(tdict['31']['sign'] + tdict['31']['data']) / dist_type
                th = float(tdict['87']['sign'] + tdict['87']['data']) / dist_type
                ih = float(tdict['88']['sign'] + tdict['88']['data']) / dist_type
            except KeyError:
                return None
            else:
                bp = BasePoint(x=0.0, y=0.0, z=0.0, ih=ih)
                p = PolarPoint(dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               angle_type=angle_type,
                               base_point=bp,
                               pid=pid,
                               text=text,
                               coordorder='NEZ'
                               )
                f = Feature(geometry=p.to_point(),
                            desc=text,
                            id=pid)
                return f
        else:
            dist_type = list(UNITS['distance'] & set(tdict.keys()))[0]
            dist_type = UNITS[tdict[dist_type]['info'][3]]
            x, y, z = [float(c) / dist_type for c in (x, y, z)]
            p = Point(x, y, z)
            f = Feature(geometry=p, desc=text, id=pid)
            return f
