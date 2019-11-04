# -*- coding: utf-8 -*-
# filename: formats/leica_gsi.py
# Copyright 2012 Stefano Costa <steko@iosa.it>
# Copyright 2015-2016 Damien Gaignon <damien.gaignon@gmail.com>

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

import logging
 
from . import Feature, Parser, Point, UNKNOWN_STATION, UNKNOWN_POINT
from .polar import BasePoint, PolarPoint

# Distance units depend of the last digit
# 0, 6 and 8 are in mm, 1/10mm and 1/100mm
# 1 and 7 are in ft and 1/10000ft converted in m
UNITS = {"angle": {'21', '22', '25'},
         "distance": {'31', '32', '33', '81', '84', '87', '88'},
         "2": "gon", "3": "deg", "4": "dms", "5": "mil",
         "0": "meter", "1": "feet", "6": "dmeter", "7": "dfeet", "8": "mmeter",
         "gon": 100000, "deg": 100000, "dms": 100000, "mil": 10000,
         "meter": 1000, "feet": 1000, "dmeter": 10000, "dfeet": 10000, "mmeter": 100000}

logger = logging.getLogger(__name__)

class FormatParser(Parser):
    '''The FormatParser for Leica GSI data format.

    Args:
        data (str): A string representing the file to be parsed.
            
    Attributes:
        line (list): A list of each lines of the file being parsed.
    '''

    def __init__(self, data):
        self.rows = data.splitlines()

    def _get_comments(self):
        """
        Get all comments of the parsed line
        
        Returns:
            A list of comments or an empty list
        """
        comments = []
        for i in range(1, 10):
            try:
                comments.append(self.tdict['4%s' % i]['data'].lstrip('0'))
            except KeyError:
                break

        return comments

    def _get_attrib(self):
        """
        Get all attributes or remarks of the parsed line
        
        Returns:
            A list of attributes and remarks or an empty list
        """
        attrib = []
        for i in range(1, 10):
            try:
                attrib.append(self.tdict['7%s' % i]['data'].lstrip('0'))
            except KeyError:
                break

        return attrib

    def _get_coordinates(self, first_coor, unit):
        """
        Get all coordinates of the parsed line
        
        Args:
            first_coor (str): The Word Index of the first coordinate.
                Could be 81 or 84
            unit (int): The divider corresponding to the coordinate unit.

        Returns:
            All three coordinates in the forme of X, Y, Z
            If these coordinates do not exist, return None
        """
        second_coor = str(int(first_coor) + 1)
        third_coor = str(int(first_coor) + 2)
        try:
            x_sign, x_data = self.tdict[first_coor]['sign'], self.tdict[first_coor]['data']
            y_sign, y_data = self.tdict[second_coor]['sign'], self.tdict[second_coor]['data']
            z_sign, z_data = self.tdict[third_coor]['sign'], self.tdict[third_coor]['data']
        except KeyError:
            x = None
            y = None
            z = None
        else:
            x = float(x_sign + x_data) / unit
            y = float(y_sign + y_data) / unit
            z = float(z_sign + z_data) / unit

        return x, y, z

    def _get_angle(self, angle, unit):
        """
        Get an angle of the parsed line
        
        Returns:
            A floating number representing the angle
            If this angle does not exist, return None
            
        """
        try:
            angle_sign, angle_data = self.tdict[angle]['sign'], self.tdict[angle]['data']
        except KeyError:
            angle = None
        else:
            angle = float(angle_sign + angle_data) / unit

        return angle

    def _get_edm_accuracy(self, ldata):
        """
        Get the ppm and the prism constant of the parsed line
        
        Returns:
            Two floating numbers representing ppm and prism constant
            If these values do not exist, return None
        """
        try:
            ppm_sign, ppm_data = self.tdict['51']['sign'], self.tdict['51']['data'][:ldata-4]
            pc_sign, pc_data = self.tdict['51']['data'][ldata-4], self.tdict['51']['data'][ldata-3:]
        except KeyError:
            try:
                ppm_sign, ppm_data = self.tdict['59']['sign'], self.tdict['59']['data']
                pc_sign, pc_data = self.tdict['58']['sign'], self.tdict['58']['data']
            except KeyError:
                ppm = None
                prism_constant = None
            else:
                ppm = float(ppm_sign + ppm_data)
                prism_constant = float(pc_sign + pc_data)
        else:
            ppm = float(ppm_sign + ppm_data)
            prism_constant = float(pc_sign + pc_data)

        return ppm, prism_constant

    def _get_value(self, value, unit):
        """
        Get a value of the parsed line
        
        Returns:
            A string value or None
        """
        try:
            value_sign, value_data = self.tdict[value]['sign'], self.tdict[value]['data']
        except KeyError:
            value = None
        else:
            value = float(value_sign + value_data) / unit

        return value

    @property
    def points(self):
        '''Extract all GSI data.

        This parser is based on the information in :ref:`if_leica_gsi`
        
        Returns:
            A list of GeoJSON-like Feature object representing points coordinates.
    
        Raises:
            KeyError: An error occured during line read, this line could not be 
                computed as the WI does not exist.
            KeyError: An error occured during computation, the data does not exist.
        
        Notes:
            Information needed are:
                - station : 11, 84, 85, 86, 88
                - direct point : 11, 81, 82, 83
                - computed point : 11, 21, 22, 31 or 32, 87 [, 88] [, 81, 82, 83]
            Angles are considered as zenithal
        '''
        
        points = []
        bp = None
        for row in self.rows:
            tokens = row.split()
            self.tdict = {}
            for t in tokens:
                t = t.lstrip('*')
                data = {
                    'wordindex': t[0:2],
                    'info': t[2:6],
                    'sign': t[6],
                    'data': t[7:],
                }
                self.tdict[data['wordindex']] = data

            try:
                pid = int(self.tdict['11']['info'])
                text = self.tdict['11']['data'].lstrip('0')
            except KeyError:
                pass
            else:
                # Get angle and distance units
                try:
                    angle_code = list(UNITS['angle'] & set(self.tdict.keys()))[0]
                    angle_unit = UNITS[self.tdict[angle_code]['info'][3]]
                except IndexError:
                    pass
                try:
                    dist_code = list(UNITS['distance'] & set(self.tdict.keys()))[0]
                    dist_unit = UNITS[self.tdict[dist_code]['info'][3]]
                except IndexError:
                    pass
                # Beginning of the parsing
                try:
                    # Look for point coordinates
                    x, y, z = self.tdict['81'], self.tdict['82'], self.tdict['83']
                except KeyError:
                    try:
                        angle, z_angle = self.tdict['21'], self.tdict['22']
                        z_angle_type = 'z'
                        # 31 or/and 32
                        try:
                            dist = self.tdict['31']
                        except KeyError:
                            try:
                                dist = self.tdict['32']
                            except KeyError:
                                logger.info('There is no distance value')
                                dist = None
                            else:
                                dist_type = 'h'
                        else:
                            dist_type = 's'
                        th = self.tdict['87']
                    except KeyError:
                        try:
                            # Look for a station
                            x, y, z = self.tdict['84'], self.tdict['85'], self.tdict['86']
                            ih = self.tdict['88']
                        except KeyError:
                            pass
                        else:
                            # Compute station data
                            x, y, z = self._get_coordinates("84", UNITS[dist_unit])
                            ih = self._get_value("88", UNITS[dist_unit])
                            bp = BasePoint(x=x, y=y, z=z, ih=ih, b_zero_st=0.0)
                            p = Point(x, y, z)
                            f = Feature(p,
                                        desc='ST',
                                        id=pid,
                                        point_name=text,
                                        dist_unit=dist_unit)
                            points.append(f)
                    else:
                        angle = self._get_angle("21", UNITS[angle_unit])
                        z_angle = self._get_angle("22", UNITS[angle_unit])
                        if dist_type == 's':
                            dist = self._get_value("31", UNITS[dist_unit])
                        else:
                            dist = self._get_value("32", UNITS[dist_unit])
                        th = self._get_value("87", UNITS[dist_unit])
                        # Polar data may have point coordinates (not used)
                        x, y, z = self._get_coordinates("81", UNITS[dist_unit])
                        # Polar data may have instrument height
                        ih = self._get_value("88", UNITS[dist_unit])
                        if ih is None:
                            ih = 0.0
                        if bp is None:
                            bp = BasePoint(x=0.0, y=0.0, z=0.0, ih=ih, b_zero_st=0.0)
                        p = PolarPoint(angle_unit=angle_unit,
                                       z_angle_type=z_angle_type,
                                       dist_type=dist_type,
                                       dist=dist,
                                       angle=angle,
                                       z_angle=z_angle,
                                       th=th,
                                       base_point=bp,
                                       pid=pid,
                                       text=text,
                                       coordorder='ENZ')
                        f = Feature(p.to_point(),
                                    desc='PT',
                                    id=pid,
                                    point_name=text)
                        points.append(f)
                else:
                    x, y, z = self._get_coordinates("81", UNITS[dist_unit])
                    p = Point(x, y, z)
                    f = Feature(p,
                                desc='PT',
                                id=pid,
                                point_name=text)
                    points.append(f)
        logger.debug(points)
        return points

    @property
    def raw_line(self):
        '''Extract all GSI data.

        This parser is based on the information in :ref:`if_leica_gsi`
        
        Returns:
            A list of GeoJSON-like Feature object representing raw data
                i.e. polar coordinates and other informations.
    
        Raises:
            KeyError: An error occured during line read, this line could not be 
                computed as the WI does not exist.
            KeyError: An error occured during computation, the data does not exist.
        
        Notes:
            Information needed are:
                - station : 11 [, 25], 84, 85, 86 [, 87], 88
                - direct point : 11, 81, 82, 83
                - computed point : 11, 21, 22, 31 or 32 [, 51], 87 [, 88] [, 81, 82, 83]
            Angles are considered as zenithal
        '''

        points = []
        # GSI files handles 8 or 16 bits data block. This will check the size
        ldata = len(self.rows[0].split()[0].lstrip('*')[7:])
        station_id = 1

        for row in self.rows:
            tokens = row.split()
            self.tdict = {}
            for t in tokens:
                t = t.lstrip('*')
                data = {
                    'wordindex': t[0:2],
                    'info': t[2:6],
                    'sign': t[6],
                    'data': t[7:],
                }
                self.tdict[data['wordindex']] = data

            try:
                pid = int(self.tdict['11']['info'])
                point_name = self.tdict['11']['data'].lstrip('0')
            except KeyError:
                try:
                    comments = self.tdict['41']
                except KeyError:
                    logger.info("The line %s will not be computed as the code '%s' is not known"\
                          % (pid, row[0:2]))
                else:
                    # Compute comments
                    comments = self._get_comments()
            else:
                # Get angle and distance units
                try:
                    angle_code = list(UNITS['angle'] & set(self.tdict.keys()))[0]
                    angle_unit = UNITS[self.tdict[angle_code]['info'][3]]
                except IndexError:
                    pass
                try:
                    dist_code = list(UNITS['distance'] & set(self.tdict.keys()))[0]
                    dist_unit = UNITS[self.tdict[dist_code]['info'][3]]
                except IndexError:
                    pass
                # Beginning of the parsing
                try:
                    # Look for a station
                    x, y, z = self.tdict['84'], self.tdict['85'], self.tdict['86']
                    ih = self.tdict['88']
                except KeyError:
                    # Otherwise look for polar data
                    try:
                        angle, z_angle = self.tdict['21'], self.tdict['22']
                        # 31 or/and 32
                        try:
                            dist = self.tdict['31']
                        except KeyError:
                            try:
                                dist = self.tdict['32']
                            except KeyError:
                                logger.info('There is no distance value')
                                dist = None
                            else:
                                dist_type = 'h'
                        else:
                            dist_type = 's'
                        th = self.tdict['87']
                    except KeyError:
                        # Otherwise look for point coordinates only
                        try:
                            x, y, z = self.tdict['81'], self.tdict['82'], self.tdict['83']
                        except KeyError:
                            # Otherwise look for Remark or Attrib
                            try:
                                attrib = self.tdict['71']
                            except KeyError:
                                # No more possibilities
                                logger.info("These data can not be compute : %s" % (self.tdict))
                            else:
                                # Compute remark or Attrib
                                attrib = self._get_attrib()
                        else:
                            # Compute point coordinates
                            x, y, z = self._get_coordinates("81", UNITS[dist_unit])
                            # Point coordinates may have remarks or attributes
                            attrib = self._get_attrib()

                            if x:
                                p = Point(x, y, z)
                            else:
                                logger.info('There is no known point')
                                p = UNKNOWN_POINT
                            f = Feature(p,
                                        desc='PT',
                                        id=pid,
                                        point_name=point_name,
                                        dist_unit=dist_unit,
                                        attrib=attrib)
                            points.append(f)
                    else:
                        # Compute polar data
                        angle = self._get_angle("21", UNITS[angle_unit])
                        z_angle = self._get_angle("22", UNITS[angle_unit])
                        z_angle_type = 'z'
                        if dist_type == 's':
                            dist = self._get_value("31", UNITS[dist_unit])
                        else:
                            dist = self._get_value("32", UNITS[dist_unit])
                        th = self._get_value("87", UNITS[dist_unit])
                        # Polar data may have point coordinates
                        x, y, z = self._get_coordinates("81",UNITS[dist_unit])
                        # Polar data may have instrument height
                        ih = self._get_value("88", UNITS[dist_unit])
                        # Polar data may have constant data
                        ppm, prism_constant = self._get_edm_accuracy(ldata)
                        # Polar data may have remarks or attributes
                        attrib = self._get_attrib()

                        if x:
                            p = Point(x, y, z)
                        else:
                            logger.info('There is no known point')
                            p = UNKNOWN_POINT

                        try:
                            station_name
                        except UnboundLocalError:
                            logger.info('There is no known station')
                            station_name = 'station_' + str(station_id)
                            station_id += 1
                        f = Feature(p,
                                    desc='PO',
                                    id=pid,
                                    point_name=point_name,
                                    angle_unit=angle_unit,
                                    z_angle_type=z_angle_type,
                                    dist_unit=dist_unit,
                                    dist_type=dist_type,
                                    angle=angle,
                                    z_angle=z_angle,
                                    dist=dist,
                                    th=th,
                                    ih=ih,
                                    ppm=ppm,
                                    prism_constant=prism_constant,
                                    st_name=station_name,
                                    attrib=attrib)
                        points.append(f)
                else:
                    # Compute station data
                    x, y, z = self._get_coordinates("84", UNITS[dist_unit])
                    ih = self._get_value("88", UNITS[dist_unit])
                    # Station data may have an azimuth angle
                    hz0 = self._get_angle("25", UNITS[angle_unit])
                    # Station data may have remarks or attributes
                    attrib = self._get_attrib()

                    if x:
                        p = Point(x, y, z)
                        station_name = point_name
                    else:
                        logger.info('There is no known station')
                        p = UNKNOWN_STATION
                        station_name = "station_" + str(station_id)
                        station_id += 1
                    f = Feature(p,
                                desc='ST',
                                id=pid,
                                point_name=point_name,
                                angle_unit=angle_unit,
                                dist_unit=dist_unit,
                                ih=ih,
                                hz0=hz0,
                                attrib=attrib)
                    points.append(f)

        logger.debug(points)
        return points
