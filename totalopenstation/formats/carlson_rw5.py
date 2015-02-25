# -*- coding: utf-8 -*-
# filename: formats/carlson_rw5.py
# Copyright 2014 Stefano Costa <steko@iosa.it>

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

from decimal import Decimal

from .polar import BasePoint, PolarPoint


class FormatParser:

    def __init__(self, data):
        self.rows = (r for r in data.splitlines() if not r.startswith('-- '))
        # Text comments, but not comment records ------------------------^

    def _points(self):
        base_points = {}
        points = []

        def record(recstr):
            fields = recstr.split(',')
            record_fields = {f[0:2] : f[2:] for f in fields[1:]}

            # Record type, including comment records
            if len(fields[0]) > 2:
                record_fields['type'] = fields[0].strip('-')
                record_fields['comment'] = True
            else:
                record_fields['type'] = fields[0]

            # Note field
            try:
                record_fields['--']
            except KeyError:
                record_fields['note'] = ''
            else:
                record_fields['note'] = record_fields['--']
            return record_fields

        for row in self.rows:
            rec = record(row)
            print(rec)
            if rec['type'] == 'OC':
                northing = float(rec['N ']) # extra whitespace
                easting = float(rec['E '])  # extra whitespace
                elevation = float(rec['EL'])
                bp = BasePoint(x=easting, y=northing, z=elevation, ih=0)
                base_points[rec['OP']] = bp
            if rec['type'] == 'BK':
                pid = rec['BP']
            if rec['type'] == 'LS':
                ih = float(rec['HI'])
                th = float(rec['HR'])
            if rec['type'] == 'SS':
                pid = rec['FP']
                angle = float(rec['AR'])
                z_angle = float(rec['ZE'])
                dist = float(rec['SD'])
                desc = rec['note']
                bp = base_points[rec['OP']]
                bp.ih = ih
                p = PolarPoint(dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               angle_type='gon',
                               base_point=bp,
                               pid=pid,
                               text=desc,
                               coordorder='NEZ')
                points.append(p.to_point().tuplepoint)
        return points

    points = property(_points)
