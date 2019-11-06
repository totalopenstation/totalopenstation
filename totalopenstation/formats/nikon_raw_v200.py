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

import logging

from . import Feature, Point, UNITS_CIRCLE, UNKNOWN_STATION, UNKNOWN_POINT, check_coordorder
from .polar import BasePoint, PolarPoint

# ussfeet = US Survey Feet
# Angular Mil is not present as the code is not known
UNITS = {"angle": {"DDDMMSS": "dms", "Gons": "gon", "Degrees": "deg"},
         "distance": {"Feet": "feet", "Metres": "meter", "Feet US": "ussfeet"}
         }

logger = logging.getLogger(__name__)


class FormatParser:
    '''The FormatParser for Nikon Raw v2.00 data.

    Args:
        data (str): A string representing the file to be parsed.

    Attributes:
        rows (list): A list of each lines of the file being parsed.
    '''

    def __init__(self, data):
        self.rows = data.splitlines()

    @property
    def points(self):
        '''Extract all Nikon RAW data format V2.00.

        This parser is based on the information in :ref:`if_nikon_raw`

        Returns:
            A list of GeoJSON-like Feature object representing points coordinates.

        Raises:

        Notes:
            Sometimes needed records are commented so it is needed to parse also comments

            Angles are considered as vertical
            Distances are slope distances
        '''
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
                        logger.info('There is no known station')
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
                    logger.info('There is no known station')
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
                               z_angle_type='v',
                               dist_type='s',
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
                               z_angle_type='v',
                               dist_type='s',
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
                               z_angle_type='v',
                               dist_type='s',
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
        logger.debug(points)
        return points

    @property
    def raw_line(self):
        '''Extract all Nikon Raw v2.00 data.

        This parser is based on the information in :ref:`if_nikon_raw`

        Returns:
            A list of GeoJSON-like Feature object representing points coordinates.

        Raises:

        Notes:
            Information needed are:
                - station : Station record
                - backsight : Control point record
                - direct point : Uploaded point or Manually input point or Calculated coordinate or Resection point
                - computed point : Sideshot, Stakeout, Face 1 or 2
  		  
           Sometimes needed records are commented so it is needed to parse also comments like
                - coordinates order
                - units

           Angles are considered as vertical
           Distances are slope distances
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
                    logger.info('There is no known station')
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
                    logger.info('There is no known station')
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
                        logger.info('There is no known point')
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
                dist = float(fs[3])
                angle = float(fs[4])
                z_angle = float(fs[5])
                try:
                    attrib = [fs[7]]
                except IndexError:
                    attrib = []
                azimuth = None
                try:
                    point = points_coord[point_name]
                except KeyError:
                    logger.info('There is no known point')
                    point = UNKNOWN_POINT
                f = Feature(point,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            z_angle_type='v',
                            dist_unit=dist_unit,
                            dist_type='s',
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            dist=dist,
                            th=th,
                            attrib=attrib)
                points.append(f)
                pid += 1
            # Look for Stakeout
            if fs[0] == 'SO':
                point_name = fs[1]
                th = float(fs[3])
                dist = float(fs[4])
                angle = float(fs[5])
                z_angle = float(fs[6])
                azimuth = None
                try:
                    point = points_coord[point_name]
                except KeyError:
                    logger.info('There is no known point')
                    point = UNKNOWN_POINT
                f = Feature(point,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            z_angle_type='v',
                            dist_unit=dist_unit,
                            dist_type='s',
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            dist=dist,
                            th=th)
                points.append(f)
                pid += 1
            # Look for Control point
            if fs[0] == 'CP':
                point_name = fs[1]
                th = float(fs[3])
                dist = float(fs[4])
                angle = float(fs[5])
                z_angle = float(fs[6])
                attrib = fs[8]
                azimuth = None
                try:
                    point = points_coord[point_name]
                except KeyError:
                    logger.info('There is no known point')
                    point = UNKNOWN_POINT
                f = Feature(point,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            z_angle_type='v',
                            dist_unit=dist_unit,
                            dist_type='s',
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            dist=dist,
                            th=th,
                            attrib=attrib)
                points.append(f)
                pid += 1
        logger.debug(points)
        return points
