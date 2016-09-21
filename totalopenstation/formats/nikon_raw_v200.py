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

from . import Feature, Point, UNITS_CIRCLE, UNKNOWN_STATION, UNKNOWN_POINT, check_coordorder
from .polar import BasePoint, PolarPoint

# ussfeet = US Survey Feet
# Angular Mil is not present as the code is not known
UNITS = {"angle": {"DDDMMSS": "dms", "Gons": "gon", "Degrees": "deg"},
         "distance": {"Feet": "feet", "Metres": "meter", "Feet US": "ussfeet"}
         }


class FormatParser:
    '''A FormatParser for Nikon RAW data format V2.00.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.'''

    def __init__(self, data):
        self.rows = data.splitlines()

    def _points(self):
        points_coord = {}
        base_points = {}
        points = []
        pid = 0
        st = 0
        cocircle = coih = False
        
        for row in self.rows:
            fs = row.split(',')
            # Get angle and distance units
            if fs[0] == 'CO':
                if fs[1].startswith('Coord Order:'):
                    coordorder = check_coordorder(fs[1].split(':')[-1].strip())
                if fs[1].startswith('Angle Units:'):
                    angle_unit = UNITS["angle"][fs[1].split(':')[1].strip()]
                if fs[1].startswith('Dist Units:'):
                    dist_unit = UNITS["distance"][fs[1].split(':')[1].strip()]
                # For fast setting, Trimble M3 can use comments for station
                if fs[1].startswith('TI  HOLD') or fs[1].startswith('TI  Hz'):
                    circle = fs[1].split('Hz')[1].strip().split()[0]
                    cocircle = True
                if fs[1].startswith('TI  INPUT'):
                    try:
                        ih = fs[1].split('ih')[1].strip().split()[0]
                    except IndexError:
                        ih = ih
                    coih = True
                if cocircle and coih:
                    station_name = "st{}".format(st)
                    try:
                        station_point = points_coord[station_name]
                    except KeyError:
                        station_point = UNKNOWN_STATION
                        points_coord[station_name] = station_point
                    f = Feature(station_point,
                            desc='ST',
                            id=pid,
                            point_name=station_name,
                            dist_unit=dist_unit,
                            ih=ih)
                    points.append(f)
                    b_zero_st = 0.0
                    bp = BasePoint(x=station_point.x, y=station_point.y, z=station_point.z, ih=ih, b_zero_st=b_zero_st)
                    base_points[station_name] = bp
                    st += 1
                    pid += 1
                    cocircle = coih = False

            # Look for point coordinates
            if fs[0] in ('UP','MP', 'CC', 'RE', 'MC'):
                point_name = fs[1]
                easting = fs[3]
                northing = fs[4]
                if coordorder == "NEZ":
                    easting, northing = northing, easting
                elevation = float(fs[5])
                point = Point(easting, northing, elevation)
                attrib = [fs[6]]
                f = Feature(point,
                            desc='PT',
                            id=pid,
                            point_name=point_name,
                            dist_unit=dist_unit,
                            attrib=attrib)
                points.append(f)
                pid += 1
                points_coord[point_name] = point
            # Look for station coordinates
            if fs[0] == 'ST':
                station_name = fs[1]
                ih = float(fs[5])
                if ih == '':
                    ih = 0
                try:
                    station_point = points_coord[station_name]
                except KeyError:
                    station_point = UNKNOWN_STATION
                    points_coord[station_name] = station_point
                # Look for back sight values in station values
                # Treat only one backsight or the last one
                if fs[3] != '':
                    b_zero_st = (float(fs[6]) - float(fs[7])) % UNITS_CIRCLE[angle_unit]
                else:
                    b_zero_st = 0.0
                f = Feature(station_point,
                            desc='ST',
                            id=pid,
                            point_name=station_name,
                            dist_unit=dist_unit,
                            ih=ih,
                            b_zero_st=b_zero_st)
                points.append(f)
                pid += 1
                bp = BasePoint(x=station_point.x, y=station_point.y, z=station_point.z, ih=ih, b_zero_st=b_zero_st)
                base_points[station_name] = bp
            # Look for Sideshot, Face 1 and Face 2
            if fs[0] in ('SS', 'F1', 'F2'):
                for i in (2, 3, 4, 5):
                    if fs[i] == '':
                        fs[i] = 0
                point_name = fs[1]
                th = float(fs[2])
                dist = float(fs[3])
                angle = float(fs[4])
                z_angle = float(fs[5])
                try:
                    attrib = [fs[7]]
                except IndexError:
                    attrib = []
                p = PolarPoint(angle_unit=angle_unit,
                               dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               base_point=bp,
                               pid=pid,
                               text=point_name,
                               coordorder=coordorder)
                point = p.to_point()
                f = Feature(point,
                            desc='PT',
                            id=pid,
                            point_name=point_name,
                            dist_unit=dist_unit,
                            attrib=attrib)
                points.append(f)
                pid += 1
                points_coord[point_name] = point
            # Look for Stakeout
            if fs[0] == 'SO':
                point_name = fs[1]
                th = float(fs[3])
                dist = float(fs[4])
                angle = float(fs[5])
                z_angle = float(fs[6])
                p = PolarPoint(angle_unit=angle_unit,
                               dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               base_point=bp,
                               pid=pid,
                               text=point_name,
                               coordorder=coordorder)
                point = p.to_point()
                f = Feature(point,
                            desc='PT',
                            id=pid,
                            point_name=point_name,
                            dist_unit=dist_unit)
                points.append(f)
                pid += 1
                points_coord[station_name] = point
            # Look for Control point
            if fs[0] == 'CP':
                point_name = fs[1]
                th = float(fs[3])
                dist = float(fs[4])
                angle = float(fs[5])
                z_angle = float(fs[6])
                attrib = [fs[8]]
                p = PolarPoint(angle_unit=angle_unit,
                               dist=dist,
                               angle=angle,
                               z_angle=z_angle,
                               th=th,
                               base_point=bp,
                               pid=pid,
                               text=point_name,
                               coordorder=coordorder)
                point = p.to_point()
                f = Feature(point,
                            desc='PT',
                            id=pid,
                            point_name=point_name,
                            dist_unit=dist_unit,
                            attrib=attrib)
                points.append(f)
                pid += 1
                points_coord[station_name] = point
        return points

    def raw_line(self):
        '''Extract all Nikon Raw v2.00 data.

        Based on the "Total Station Nivo Series - Nivo3.M and Nivo5.M" document.

        Information needed are:
            - station :
            - backsight :
            - direct point :
            - computed point :

        Units are unchanged, format of the original parsed file

        TODO:
            - add all missing code
            - get comments
            - add the possibility to customize code
        '''
        points_coord = {}
        points = []
        pid = 0
        st = 0
        cocircle = coih = False

        for row in self.rows:
            fs = row.split(',')
            # Get angle and distance units
            if fs[0] == 'CO':
                if fs[1].startswith('Coord Order:'):
                    coordorder = check_coordorder(fs[1].split(':')[-1].strip())
                if fs[1].startswith('Angle Units:'):
                    angle_unit = UNITS["angle"][fs[1].split(':')[1].strip()]
                if fs[1].startswith('Dist Units:'):
                    dist_unit = UNITS["distance"][fs[1].split(':')[1].strip()]
                # For fast setting, Trimble M3 can use comments for station
                if fs[1].startswith('TI  HOLD') or fs[1].startswith('TI  Hz'):
                    circle = fs[1].split('Hz')[1].strip().split()[0]
                    cocircle = True
                if fs[1].startswith('TI  INPUT'):
                    try:
                        ih = fs[1].split('ih')[1].strip().split()[0]
                    except IndexError:
                        ih = ih
                    coih = True
            if cocircle and coih:
                station_name = "st{}".format(st)
                try:
                    station_point = points_coord[station_name]
                except KeyError:
                    station_point = UNKNOWN_STATION
                    points_coord[station_name] = station_point
                f = Feature(station_point,
                        desc='ST',
                        id=pid,
                        point_name=station_name,
                        dist_unit=dist_unit,
                        ih=ih)
                points.append(f)
                st += 1
                pid += 1
                cocircle = coih = False

            # Look for point coordinates
            if fs[0] in ('UP','MP', 'CC', 'RE', 'MC'):
                point_name = fs[1]
                easting = fs[3]
                northing = fs[4]
                if coordorder == "NEZ":
                    easting, northing = northing, easting
                elevation = float(fs[5])
                point = Point(easting, northing, elevation)
                attrib = [fs[6]]
                f = Feature(point,
                            desc='PT',
                            id=pid,
                            point_name=point_name,
                            dist_unit=dist_unit,
                            attrib=attrib)
                points.append(f)
                pid += 1
                points_coord[point_name] = point
            # Look for station coordinates
            if fs[0] == 'ST':
                station_name = fs[1]
                ih = float(fs[5])
                if ih == '':
                    ih = 0
                try:
                    station_point = points_coord[station_name]
                except KeyError:
                    station_point = UNKNOWN_STATION
                    points_coord[station_name] = station_point
                f = Feature(station_point,
                            desc='ST',
                            id=pid,
                            point_name=station_name,
                            dist_unit=dist_unit,
                            ih=ih)
                points.append(f)
                pid += 1
                # Look for back sight values in station values
                # Treat only one backsight or the last one
                if fs[3] != '':
                    b_zero_st = (float(fs[6]) - float(fs[7])) % UNITS_CIRCLE[angle_unit]
                else:
                    b_zero_st = 0.0
                if fs[3] != '':
                    point_name = fs[3]
                    azimuth = fs[6]
                    circle = fs[7]
                    try:
                        point = points_coord[point_name]
                    except KeyError:
                        point = UNKNOWN_POINT
                    f = Feature(point,
                                desc='BS',
                                id=pid,
                                point_name=point_name,
                                angle_unit=angle_unit,
                                circle=circle,
                                azimuth=azimuth)
                    points.append(f)
                    pid += 1
            # Look for Sideshot, Face 1 and Face 2
            if fs[0] in ('SS', 'F1', 'F2'):
                for i in (2, 3, 4, 5):
                    if fs[i] == '':
                        fs[i] = 0
                point_name = fs[1]
                th = float(fs[2])
                slope_dist = float(fs[3])
                angle = float(fs[4])
                z_angle = float(fs[5])
                try:
                    attrib = [fs[7]]
                except IndexError:
                    attrib = []
                azimuth = None
                horizontal_dist = None
                try:
                    point = points_coord[point_name]
                except KeyError:
                    point = UNKNOWN_POINT
                f = Feature(point,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            dist_unit=dist_unit,
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            slope_dist=slope_dist,
                            horizontal_dist=horizontal_dist,
                            th=th,
                            attrib=attrib)
                points.append(f)
                pid += 1
            # Look for Stakeout
            if fs[0] == 'SO':
                point_name = fs[1]
                th = float(fs[3])
                slope_dist = float(fs[4])
                angle = float(fs[5])
                z_angle = float(fs[6])
                azimuth = None
                horizontal_dist = None
                try:
                    point = points_coord[point_name]
                except KeyError:
                    point = UNKNOWN_POINT
                f = Feature(point,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            dist_unit=dist_unit,
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            slope_dist=slope_dist,
                            horizontal_dist=horizontal_dist,
                            th=th)
                points.append(f)
                pid += 1
            # Look for Control point
            if fs[0] == 'CP':
                point_name = fs[1]
                th = float(fs[3])
                slope_dist = float(fs[4])
                angle = float(fs[5])
                z_angle = float(fs[6])
                attrib = fs[8]
                azimuth = None
                horizontal_dist = None
                try:
                    point = points_coord[point_name]
                except KeyError:
                    point = UNKNOWN_POINT
                f = Feature(point,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            dist_unit=dist_unit,
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            slope_dist=slope_dist,
                            horizontal_dist=horizontal_dist,
                            th=th,
                            attrib=attrib)
                points.append(f)
                pid += 1
        return points


    points = property(_points)
