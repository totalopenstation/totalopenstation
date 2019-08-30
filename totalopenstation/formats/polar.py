# -*- coding: utf-8 -*-
# filename: polar.py
# Copyright 2010, 2014 Stefano Costa <steko@iosa.it>
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

from math import cos, sin, tan

from totalopenstation.formats.conversion import to_rad
from . import Feature, Point, UNITS_CIRCLE


def polar_to_cartesian(angle_unit, z_angle_type, dist_type, base_x, base_y, base_z, dist, azimuth, z_angle, ih, th):
    '''Convert polar coordinates to cartesian.

    Needs base point coordinates, measurement angles and distance.
    Angles must be given in radians.

    Some important caveats of the current implementation:

    - the horizontal ``angle`` is hardcoded with zero azimuth at North
    '''

    if z_angle_type == 'dh':
        dZ = z_angle
    if z_angle_type == 'v':
        if dist_type == 'h':
            dZ = dist * tan(to_rad(z_angle, angle_unit))
        else:
            dZ = dist * sin(to_rad(z_angle, angle_unit))
    if z_angle_type == 'z':
        if dist_type == 'h':
            dZ = dist / tan(to_rad(z_angle, angle_unit))
        else:
            dZ = dist * cos(to_rad(z_angle, angle_unit))
    if dist_type == 's':
        if z_angle_type == 'dh':
            dist = (dist ** 2 - z_angle ** 2) ** (0.5)
        if z_angle_type == 'v':
            dist = dist * cos(to_rad(z_angle, angle_unit))
        if z_angle_type == 'z':
            dist = dist *  sin(to_rad(z_angle, angle_unit))
    dX = dist * sin(to_rad(azimuth, angle_unit))
    dY = dist * cos(to_rad(azimuth, angle_unit))

    target_x = base_x + dX
    target_y = base_y + dY
    target_z = base_z + ih + dZ - th

    return dict(x=target_x, y=target_y, z=target_z)


class PolarPoint:
    '''A point geometry defined by polar coordinates.'''

    def __init__(self,
                 angle_unit,          # angle unit
                 z_angle_type,        # type of angle z, v or dh
                 dist_type,           # type of distance h or s
                 dist,                # inclined distance
                 angle,               # horizontal angle
                 z_angle,             # vertical angle
                 th,                  # target height
                 base_point,          # BasePoint object
                 pid,                 # point ID
                 text,                # point description
                 coordorder):   # cartesian coordinates order (NEZ, ENZ)
        self.angle_unit = angle_unit
        self.z_angle_type = z_angle_type
        self.dist_type = dist_type
        self.dist = float(dist)
        self.th = float(th)
        self.angle = float(angle)
        self.z_angle = float(z_angle)
        self.pid = pid
        self.text = text
        self.coordorder = coordorder

        # base point data
        self.base_x = base_point.x
        self.base_y = base_point.y
        # For NEZ coordinate system, an inversion should be done before calculation
        if self.coordorder == "NEZ":
            self.base_x, self.base_y = self.base_y, self.base_x
        self.base_z = base_point.z
        self.ih = base_point.ih
        self.b_zero_st = base_point.b_zero_st

    def to_point(self):
        '''Convert from PolarPoint to (cartesian) Point object'''

        azimuth = (self.b_zero_st + self.angle) % UNITS_CIRCLE[self.angle_unit]

        cart_coords = polar_to_cartesian(self.angle_unit,
                                         self.z_angle_type,
                                         self.dist_type,
                                         self.base_x,
                                         self.base_y,
                                         self.base_z,
                                         self.dist,
                                         azimuth,
                                         self.z_angle,
                                         self.ih,
                                         self.th)

        if self.coordorder == "NEZ":
            cart_coords['x'], cart_coords['y'] = cart_coords['y'], cart_coords['x']

        cart_point = Point(cart_coords['x'],
                           cart_coords['y'],
                           cart_coords['z'])

        return cart_point

    def as_feature(self):
        '''Wrap geometry and other properties like id, description in a Feature.'''

        feature = Feature(self.to_point(),
                          properties={'angle_unit': self.angle_unit},
                          id=self.pid,
                          desc=self.desc)
        return feature


class BasePoint:
    '''A base point to derive cartesian coordinates from polar.

    TODO: find out whether ih is more commonly coupled to a base point or
    to each single point.'''

    def __init__(self, x, y, z, ih, b_zero_st):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.ih = float(ih)
        self.b_zero_st = float(b_zero_st)
