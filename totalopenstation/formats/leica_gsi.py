# -*- coding: utf-8 -*-
# filename: formats/leica_gsi.py
# Copyright 2012 Stefano Costa <steko@iosa.it>
# Copyright 2015 Damien Gaignon <damien.gaignon@gmail.com>

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
from totalopenstation.utils.conversion import dms_to_gon, deg_to_gon, \
    mil_to_gon, horizontal_to_slope
from totalopenstation.formats.landxml import Survey

# Distance units depend of the last digit
# 0, 6 and 8 are in mm, 1/10mm and 1/100mm
# 1 and 7 are in ft and 1/10000ft converted in m
UNITS = {"angle": {'21', '22', '25'},
         "distance": {'31', '32', '33', '81', '84', '87', '88'},
         "2": "gon", "3": "deg", "4": "dms", "5": "mil",
         "0": "meter", "1": "feet", "6": "dmeter", "7": "dfeet", "8": "mmeter",
         "meter": 1000, "feet": 1000 / 3.28084, "dmeter": 10000, "dfeet": 10000 / 3.28084, "mmeter": 100000}


class FormatParser(Parser):
    """
    A FormatParser for Leica GSI data format.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.
    """

    def __init__(self, data):
        self.line = data.splitlines()

    def _get_comments(self):
        """
        Get all comments of the parsed line
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
        """
        attrib = []
        for i in range(1, 10):
            try:
                attrib.append(self.tdict['7%s' % i]['data'].lstrip('0'))
            except KeyError:
                break

        return attrib

    def _get_coordinates(self, first_coor, units):
        """
        Get all coordinates of the parsed line
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
            x = float(x_sign + x_data) / units
            y = float(y_sign + y_data) / units
            z = float(z_sign + z_data) / units

        return x, y, z

    def _get_angle(self, angle, units, ldata):
        """
        Get an angle of the parsed line
        """
        try:
            angle_sign, angle_data = self.tdict[angle]['sign'], self.tdict[angle]['data']
        except KeyError:
            angle = None
        else:
            if units == "dms":
                angle = dms_to_gon({"D": angle_sign + angle_data[:ldata - 5],
                                    "M": angle_data[ldata - 5:ldata - 3],
                                    "S": angle_data[ldata - 3:ldata - 1],
                                    "milliseconds": angle_data[ldata - 1:]})
            elif units == "mil":
                angle = mil_to_gon(float(angle_sign + angle_data) / 10000)
            elif units == "deg":
                angle = deg_to_gon(float(angle_sign + angle_data) / 100000)
            else:
                angle = float(angle_sign + angle_data) / 100000

        return angle

    def _get_edm_accuracy(self, ldata):
        """
        Get the ppm and the prism constant of the parsed line
        """
        try:
            ppm_sign, ppm_data = self.tdict['51']['sign'], self.tdict['51']['data'][:ldata - 4]
            pc_sign, pc_data = self.tdict['51']['data'][ldata - 4], self.tdict['51']['data'][ldata - 3:]
        except KeyError:
            try:
                ppm_sign, ppm_data = self.tdict['59']['sign'], self.tdict['59']['data']
                pc_sign, pc_data = self.tdict['58']['data'][4], self.tdict['58']['data']
            except KeyError:
                ppm = None
                prism_constant = None
        if ppm_sign:
            ppm = float(ppm_sign + ppm_data) / 10
        if pc_sign:
            prism_constant = float(pc_sign + pc_data) / 10000

        return ppm, prism_constant

    def _get_value(self, value, units):
        """
        Get a value of the parsed line
        """
        try:
            value_sign, value_data = self.tdict[value]['sign'], self.tdict[value]['data']
        except KeyError:
            value = None
        else:
            value = float(value_sign + value_data) / units

        return value

    def _points(self):
        survey = Survey()

        bp = None
        ldata = len(self.line[0].split()[0].lstrip('*')[7:])
        for line in self.line:
            tokens = line.split()
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
                pid = self.tdict['11']['info']
                text = self.tdict['11']['data'].lstrip('0')
            except KeyError:
                pass
            else:
                # Get angle and distance units
                try:
                    angle_code = list(UNITS['angle'] & set(self.tdict.keys()))[0]
                    angle_units = UNITS[self.tdict[angle_code]['info'][3]]
                except IndexError:
                    pass
                try:
                    dist_code = list(UNITS['distance'] & set(self.tdict.keys()))[0]
                    dist_units = UNITS[self.tdict[dist_code]['info'][3]]
                except IndexError:
                    pass
                # Beginning of the parsing
                try:
                    # Look for point coordinates
                    x, y, z = self.tdict['81'], self.tdict['82'], self.tdict['83']
                except KeyError:
                    try:
                        angle, z_angle = self.tdict['21'], self.tdict['22']
                        # 31 or/and 32
                        try:
                            slope_dist = self.tdict['31']
                        except KeyError:
                            slope_dist = None
                        try:
                            horizontal_dist = self.tdict['32']
                        except KeyError:
                            horizontal_dist = None
                        if horizontal_dist is None and slope_dist is None:
                            raise KeyError
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
                            x, y, z = self._get_coordinates("84", UNITS[dist_units])
                            ih = self._get_value("88", UNITS[dist_units])
                            bp = BasePoint(x=x, y=y, z=z, ih=ih)
                            survey.cg_point(point_name=text,
                                            pid=pid,
                                            x=x,
                                            y=y,
                                            z=z,
                                            attrib=["Station"])
                    else:
                        angle = self._get_angle("21", angle_units, ldata)
                        z_angle = self._get_angle("22", angle_units, ldata)
                        if slope_dist:
                            slope_dist = self._get_value("31", UNITS[dist_units])
                        if horizontal_dist:
                            horizontal_dist = self._get_value("32", UNITS[dist_units])
                            # Need to convert horizontal distance to slope distance
                            slope_dist = horizontal_to_slope(horizontal_dist, z_angle)
                        th = self._get_value("87", UNITS[dist_units])
                        # Polar data may have point coordinates (not used)
                        x, y, z = self._get_coordinates("81", UNITS[dist_units])
                        # Polar data may have instrument height
                        ih = self._get_value("88", UNITS[dist_units])
                        if ih is None:
                            ih = 0.0
                        if bp is None:
                            bp = BasePoint(x=0.0, y=0.0, z=0.0, ih=ih)
                        p = PolarPoint(dist=slope_dist,
                                       angle=angle,
                                       z_angle=z_angle,
                                       th=th,
                                       base_point=bp,
                                       pid=pid,
                                       text=text,
                                       coordorder='NEZ')
                        point = p.to_point()
                        survey.cg_point(point_name=text,
                                        pid=pid,
                                        x=point.x,
                                        y=point.y,
                                        z=point.z,
                                        attrib=["Point"])
                else:
                    x, y, z = self._get_coordinates("81", UNITS[dist_units])
                    survey.cg_point(point_name=text,
                                    pid=pid,
                                    x=x,
                                    y=y,
                                    z=z,
                                    attrib=["Point"])
        return survey

    def raw_line(self):
        """
        Extract all GSI data.

        Based on the "GSI ONLINE for Leica TPS" document.

        Information needed are:
            - station : 11 [, 25], 84, 85, 86 [, 87], 88
            - direct point : 11, 81, 82, 83
            - computed point : 11, 21, 22, 31 or 32 [, 51], 87 [, 88] [, 81, 82, 83]

        Units after computation:
            - angle in gon
            - distance in meter

        TODO:
            - get coordinates order (NEZ or ENZ)
            - add all missing code
            - get comments
            - add an option to link the comment to either previous or next line
            - add the possibility to customize code
        """

        survey = Survey()
        ldata = len(self.line[0].split()[0].lstrip('*')[7:])

        for line in self.line:
            tokens = line.split()
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
                pid = self.tdict['11']['info']
                text = self.tdict['11']['data'].lstrip('0')
            except KeyError:
                try:
                    comments = self.tdict['41']
                except KeyError:
                    print("The line %s will not be computed as the code '%s' is not known") \
                         % (pid, line[0:2])
                else:
                    # Compute comments
                    comments = self._get_comments()
            else:
                # Get angle and distance units
                try:
                    angle_code = list(UNITS['angle'] & set(self.tdict.keys()))[0]
                    angle_units = UNITS[self.tdict[angle_code]['info'][3]]
                except IndexError:
                    pass
                try:
                    dist_code = list(UNITS['distance'] & set(self.tdict.keys()))[0]
                    dist_units = UNITS[self.tdict[dist_code]['info'][3]]
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
                            slope_dist = self.tdict['31']
                        except KeyError:
                            slope_dist = None
                        try:
                            horizontal_dist = self.tdict['32']
                        except KeyError:
                            horizontal_dist = None
                        if horizontal_dist is None and slope_dist is None:
                            raise KeyError
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
                                raise KeyError("These data can not be compute.")
                            else:
                                # Compute remark or Attrib
                                attrib = self._get_attrib()
                        else:
                            # Compute point coordinates
                            x, y, z = self._get_coordinates("81", UNITS[dist_units])
                            # Point coordinates may have remarks or attributes
                            attrib = self._get_attrib()

                            survey.cg_point(point_name=text,
                                            pid=pid,
                                            x=x,
                                            y=y,
                                            z=z)
                    else:
                        # Compute polar data
                        angle = self._get_angle("21", angle_units, ldata)
                        z_angle = self._get_angle("22", angle_units, ldata)
                        if slope_dist:
                            slope_dist = self._get_value("31", UNITS[dist_units])
                        if horizontal_dist:
                            horizontal_dist = self._get_value("32", UNITS[dist_units])
                        th = self._get_value("87", UNITS[dist_units])
                        # Polar data may have point coordinates
                        x, y, z = self._get_coordinates("81", UNITS[dist_units])
                        # Polar data may have instrument height
                        ih = self._get_value("88", UNITS[dist_units])
                        # Polar data may have constant data
                        ppm, prism_constant = self._get_edm_accuracy(ldata)
                        # Polar data may have remarks or attributes
                        attrib = self._get_attrib()

                        survey.raw_observation(pid=pid,
                                               point_name=text,
                                               angle=angle,
                                               z_angle=z_angle,
                                               slope_dist=slope_dist,
                                               horizontal_dist=horizontal_dist,
                                               th=th,
                                               ih=ih,
                                               ppm=ppm,
                                               prism_constant=prism_constant,
                                               x=x,
                                               y=y,
                                               z=z,
                                               attrib=attrib)
                else:
                    # Compute station data
                    x, y, z = self._get_coordinates("84", UNITS[dist_units])
                    ih = self._get_value("88", UNITS[dist_units])
                    # Station data may have an azimuth angle
                    hz0 = self._get_angle("25", angle_units, ldata)
                    # Station data may have remarks or attributes
                    attrib = self._get_attrib()

                    survey.setup(pid=pid,
                                 point_name=text,
                                 ih=ih,
                                 hz0=hz0,
                                 instru_x=x,
                                 instru_y=y,
                                 instru_z=z,
                                 attrib=attrib)

        return survey

    points = property(_points)
