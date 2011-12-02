# -*- coding: utf-8 -*-
# filename: polar.py
# Copyright 2010 Stefano Costa <steko@iosa.it>

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

import math

from . import Point


def polar_to_cartesian(base_x, base_y, base_z, dist, angle, z_angle, ih, th):
    '''Convert polar coordinates to cartesian.

    Needs both base point coordinates and measurement angle and distance.
    Angles should be given in radiants.'''

    rad_angle = angle
    rad_z_angle = z_angle
    dist_r = math.sin(rad_z_angle) * dist
    target_x = base_x + math.cos(rad_angle) * dist_r
    target_y = base_y + math.sin(rad_angle) * dist_r
    target_z = base_z + math.cos(rad_z_angle) * dist
    target_z = target_z + ih - th
    return dict(x=target_x, y=target_y, z=target_z)


class PolarPoint:
    '''A point geometry defined by polar coordinates.'''

    def __init__(self,
                 dist,                # inclined distance
                 angle,               # horizontal angle
                 z_angle,             # vertical angle
                 th,                  # target height
                 angle_type,          # degrees or gons
                 base_point,          # BasePoint object
                 pid,                 # point ID
                 text,                # point description
                 coordorder='NEZ'):   # cartesian coordinates order (NEZ, ENZ)
        self.dist = float(dist)
        self.th = float(th)
        self.angle_type = angle_type
        if angle_type is 'deg':
            self.angle = math.radians(float(angle))
            self.z_angle = math.radians(float(z_angle))
        if angle_type is 'gon':
            self.angle = math.radians(float(angle)*0.9)
            self.z_angle = math.radians(float(z_angle)*0.9)
        self.pid = pid
        self.text = text
        self.coordorder = coordorder
        # base point data
        self.base_x = base_point.x
        self.base_y = base_point.y
        self.base_z = base_point.z
        self.ih = base_point.ih

    def to_cartesian(self):
        '''Converts from polar to cartesian.'''

        coords = polar_to_cartesian(self.base_x,
                                    self.base_y,
                                    self.base_z,
                                    self.dist,
                                    self.angle,
                                    self.z_angle,
                                    self.ih,
                                    self.th)
        return "%(x)s,%(y)s,%(z)s" % coords

    def to_point(self):
        '''Convert from PolarPoint to (cartesian) Point object'''

        cart_coords = polar_to_cartesian(self.base_x,
                                    self.base_y,
                                    self.base_z,
                                    self.dist,
                                    self.angle,
                                    self.z_angle,
                                    self.ih,
                                    self.th)

        if self.coordorder == 'NEZ':
            cart_coords['x'], cart_coords['y'] = cart_coords['y'], cart_coords['x']

        cart_point = Point(self.pid,
                           cart_coords['x'],
                           cart_coords['y'],
                           cart_coords['z'],
                           self.text)

        return cart_point.tuplepoint


class BasePoint:
    '''A base point to derive cartesian coordinates from polar.

    TODO: find out whether ih is more commonly coupled to a base point or
    to each single point.'''

    def __init__(self, x, y, z, ih):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.ih = float(ih)
