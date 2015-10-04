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
    '''A FormatParser for Leica GSI data format.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.'''

    def __init__(self, data):
        self.line = data.splitlines()

    def _points(self):
        points = []
        bp = None
        for line in self.line:
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
                pass
            else:
                try:
                    x = tdict['81']['sign'] + tdict['81']['data']
                    y = tdict['82']['sign'] + tdict['82']['data']
                    z = tdict['83']['sign'] + tdict['83']['data']
                except KeyError:
                    try:
                        angle_code = list(UNITS['angle'] & set(tdict.keys()))[0]
                        angle_units = UNITS[tdict[angle_code]['info'][3]]
                        if angle_units == "dms":
                            angle_data = tdict['21']['data']
                            if len(angle_data) == 8:
                                angle = {"D": tdict['21']['sign'] + angle_data[:3],
                                         "M": angle_data[3:5],
                                         "S": angle_data[5:7],
                                         "milliseconds": angle_data[7:]}
                            else:
                                angle = {"D": tdict['21']['sign'] + angle_data[:11],
                                         "M": angle_data[11:13],
                                         "S": angle_data[13:15],
                                         "milliseconds": angle_data[15:]}
                            z_angle_data = tdict['22']['data']
                            if len(z_angle_data) == 8:
                                z_angle = {"D": tdict['21']['sign'] + z_angle_data[:3],
                                           "M": z_angle_data[3:5],
                                           "S": z_angle_data[5:7],
                                           "milliseconds": z_angle_data[7:]}
                            else:
                                z_angle = {"D": tdict['21']['sign'] + z_angle_data[:11],
                                           "M": z_angle_data[11:13],
                                           "S": z_angle_data[13:15],
                                           "milliseconds": z_angle_data[15:]}
                        elif angle_units == "mil":
                            angle = float(tdict['21']['sign'] + tdict['21']['data'])/10000
                            z_angle = float(tdict['22']['sign'] + tdict['22']['data'])/10000
                        else:
                            angle = float(tdict['21']['sign'] + tdict['21']['data'])/100000
                            z_angle = float(tdict['22']['sign'] + tdict['22']['data'])/100000
                        dist_code = list(UNITS['distance'] & set(tdict.keys()))[0]
                        dist_units = UNITS[tdict[dist_code]['info'][3]]
                        dist = float(tdict['31']['sign'] + tdict['31']['data'])/dist_units
                        th = float(tdict['87']['sign'] + tdict['87']['data'])/dist_units
                        # Instrument high should not be on the measurement line but on the station line
                        # ih could be on measurement line without station line before because of the use of quick settings
                        # base point: x=0.0, y=0.0, z=0.0, ih=ih
                        # if possible manual investigation should be perform to compute all coordinates
                        try:
                            ih = float(tdict['88']['sign'] + tdict['88']['data'])/dist_units
                        # In case no station line exist, initialize ih but every coordinates of the point would not be correct
                        # base point: x=0.0, y=0.0, z=0.0, ih=0.0
                        # if possible manual investigation should be perform to compute all coordinates
                        except KeyError:
                            ih = 0.0
                    except KeyError:
                        try:
                            dist_code = list(UNITS['distance'] & set(tdict.keys()))[0]
                            dist_units = UNITS[tdict[dist_code]['info'][3]]
                            xst = float(tdict['84']['sign'] + tdict['84']['data'])/dist_units
                            yst = float(tdict['85']['sign'] + tdict['85']['data'])/dist_units
                            zst = float(tdict['86']['sign'] + tdict['86']['data'])/dist_units
                            ih = float(tdict['88']['sign'] + tdict['88']['data'])/dist_units
                        except KeyError:
                            pass
                        else:
                            bp = BasePoint(x=xst, y=yst, z=zst, ih=ih)
                    else:
                        if bp is None:
                            bp = BasePoint(x=0.0, y=0.0, z=0.0, ih=ih)
                        p = PolarPoint(dist=dist,
                                       angle=angle,
                                       z_angle=z_angle,
                                       th=th,
                                       angle_type=angle_units,
                                       base_point=bp,
                                       pid=pid,
                                       text=text,
                                       coordorder='NEZ'
                                       )
                        f = Feature(geometry=p.to_point(),
                                    desc=text,
                                    id=pid)
                        points.append(f)
                else:
                    dist_code = list(UNITS['distance'] & set(tdict.keys()))[0]
                    dist_units = UNITS[tdict[dist_code]['info'][3]]
                    x, y, z = [float(c)/dist_units for c in (x, y, z)]
                    p = Point(x, y, z)
                    f = Feature(geometry=p, desc=text, id=pid)
                    points.append(f)
        return points

    points = property(_points)
