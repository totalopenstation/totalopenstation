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

from . import Parser, Point
from polar import BasePoint, PolarPoint


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
                #angle_type = tdict['21']['info']
                angle = float(tdict['21']['sign'] + tdict['21']['data'])/100000
                z_angle = float(tdict['22']['sign'] + tdict['22']['data'])/100000
                dist = float(tdict['31']['sign'] + tdict['31']['data'])/1000
                th = float(tdict['87']['sign'] + tdict['87']['data'])/1000
                ih = float(tdict['88']['sign'] + tdict['88']['data'])/1000
            except KeyError:
                return None
            else:
                bp = BasePoint(x=0.0, y=0.0, z=0.0, ih=ih)
                p = PolarPoint(dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               angle_type='deg',
                               base_point=bp,
                               pid=pid,
                               text=text,
                               coordorder='NEZ'
                               )
                return p.to_point()
        else:
            x, y, z = [float(c)/1000 for c in (x, y, z)]
            p = Point(pid, x, y, z, text)
            return p
