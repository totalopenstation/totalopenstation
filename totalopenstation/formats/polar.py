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

def deg2rad(deg):
    '''Convert degrees to radiants.'''

    rad = deg / 180.0 * math.pi
    return rad


def gon2rad(gon):
    '''Convert gons to radiants ( 400 gon = 360° )'''


    rad = gon / 200.0 * math.pi
    return rad


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

    def __init__(self, dist, angle, z_angle, th, angle_type, base_point):
        self.dist = dist
        self.th = th
        self.angle_type = angle_type
        if angle_type is 'deg':
            self.angle = deg2rad(angle)
            self.z_angle = deg2rad(z_angle)
        if angle_type is 'gon':
            self.angle = gon2rad(angle)
            self.z_angle = gon2rad(z_angle)
        # base point data
        self.base_x = base_point.x
        self.base_y = base_point.y
        self.base_z = base_point.z
        self.ih = base_point.ih

    def to_cartesian(self):
        '''Converts from polar to cartesian.'''

        return polar_to_cartesian(self.base_x,
                                  self.base_y,
                                  self.base_z,
                                  self.dist,
                                  self.angle,
                                  self.z_angle,
                                  self.ih,
                                  self.th)


class BasePoint:
    '''A base point to derive cartesian coordinates from polar.

    TODO: find out whether ih is more commonly coupled to a base point or
    to each single point.'''

    def __init__(self, x, y, z, ih):
        self.x = x
        self.y = y
        self.z = z
        self.ih = ih


if __name__ == '__main__':
    bp0 = BasePoint(x=100.0, y=100.0, z=100.0, ih=0)

    p0 = PolarPoint(dist=10,
                    angle=0,
                    z_angle=0,
                    th=0,
                    angle_type='deg',
                    base_point=bp0)
    print p0.to_cartesian()
