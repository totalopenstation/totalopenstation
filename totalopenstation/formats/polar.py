# -*- coding: utf-8 -*-
# filename: polar.py
# Copyright 2010, 2014 Stefano Costa <steko@iosa.it>

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

from math import cos, sin, radians

from . import Point


def polar_to_cartesian(base_x, base_y, base_z, dist, angle, z_angle, ih, th):
    '''Convert polar coordinates to cartesian.

    Needs base point coordinates, measurement angles and distance.
    Angles must be given in radians.

    Some important caveats of the current implementation:

    - the horizontal ``angle`` is hardcoded with zero azimuth at North
    - the vertical ``z_angle`` is hardcoded with zero at zenith
    '''

    dist_r = sin(z_angle) * dist
    target_x = base_x + cos(angle) * dist_r
    target_y = base_y + sin(angle) * dist_r
    target_z = base_z + ih + (cos(z_angle) * dist) - th

    return dict(x=target_x, y=target_y, z=target_z)


class PolarPoint:
    '''A point geometry defined by polar coordinates.'''

    COORDINATE_ORDER = ('NEZ', 'ENZ')

    def __init__(self,
                 dist,                # inclined distance
                 angle,               # horizontal angle
                 z_angle,             # vertical angle
                 th,                  # target height
                 angle_type,          # degrees or gons
                 base_point,          # BasePoint object
                 pid,                 # point ID
                 text,                # point description
                 coordorder):   # cartesian coordinates order (NEZ, ENZ)
        self.dist = float(dist)
        angle = float(angle)
        z_angle = float(z_angle)
        self.th = float(th)
        self.angle_type = angle_type
        if angle_type == 'deg':
            self.angle = radians(angle)
            self.z_angle = radians(z_angle)
        if angle_type == 'gon':
            self.angle = radians(angle * 0.9)
            self.z_angle = radians(z_angle * 0.9)
        self.pid = pid
        self.text = text
        if any((coordorder == v for v in PolarPoint.COORDINATE_ORDER)):
            self.coordorder = coordorder
        else:
            raise ValueError('Invalid coordinate order')
        # base point data
        self.base_x = base_point.x
        self.base_y = base_point.y
        self.base_z = base_point.z
        self.ih = base_point.ih

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

        return cart_point


class BasePoint:
    '''A base point to derive cartesian coordinates from polar.

    TODO: find out whether ih is more commonly coupled to a base point or
    to each single point.'''

    def __init__(self, x, y, z, ih):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.ih = float(ih)
