#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_txt.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com>
# Copyright 2008,2011 Stefano Costa <steko@iosa.it>
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

from math import cos, sin, radians, pi

def deg_to_gon(angle):
    '''Convert degrees format to grade (gon) format.'''
    return angle * 400 / 360

def deg_to_rad(angle):
    '''Convert degrees format to radian format.'''
    return radians(angle)

def dms_to_gon(angle):
    '''Convert degrees in DDD.MMSS format to grade (gon) format.'''

    angle = float(angle["D"]) + float(angle["M"]) / 60 + float(angle["S"]) / 3600 + \
            float(angle["milliseconds"]) / 1000
    return deg_to_gon(angle)

def dms_to_rad(angle):
    '''Convert degrees in DDD.MMSS format to radians format.'''

    angle = float(angle["D"]) + float(angle["M"]) / 60 + float(angle["S"]) / 3600 + \
            float(angle["milliseconds"]) / 1000
    return deg_to_rad(angle)

def mil_to_gon(angle):
    '''Convert degrees in mil (NATO) format to grade (gon) format.'''
    return angle * 400 / 6400

def mil_to_rad(angle):
    '''Convert degrees in mil (NATO) format to radian format.'''
    return angle * 2 * pi / 6400

def gon_to_rad(angle):
    '''Convert grade (gon) format to radian format.'''
    return angle * 2 * pi / 400

def horizontal_to_slope(dist, angle):
    return dist / sin (gon_to_rad(angle))