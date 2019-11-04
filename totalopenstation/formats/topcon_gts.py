# -*- coding: utf-8 -*-
# filename: formats/topcon_gts.py
# Copyright 2010 Stefano Costa <steko@iosa.it>
# Copyright 2010 Cristiano Moscaritolo <cristianomoscaritolo@yahoo.it>
# Copyright 2010 Olga Pastore <olga.pastore@gmail.com>
# Copyright 2010 Enza Battiante <enza.battiante@alice.it>
# Copyright 2010 Raffaele Fanelli <rfl.fanelli@libero.it>
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

from .polar import BasePoint, PolarPoint
from totalopenstation.formats.conversion import deg_to_gon
from . import Feature

logger = logging.getLogger(__name__)


class FormatParser:
    '''A FormatParser for Topcon GTS polar format.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.'''

    def __init__(self, data):
        # workaround for (apparently) corrupt downloaded data
        clean_data = ''.join([l[1:-5] for l in data.splitlines()])
        self.rows = clean_data.split(',')

    @property
    def points(self):
        points = []
        bp = BasePoint(x=0, y=0, z=0, ih=0, b_zero_st=0.0 )
        for row in self.rows:
            fs = row.split('+')
            try:
                pid = fs[1][:-3]
            except IndexError:
                continue
            text = fs[-1][0:5]
            try:
                th = float(fs[0][:-1])
            except ValueError:
                continue
            coordorder = 'NEZ'
            dist = float(fs[2].split('m')[0])
            angle = deg_to_gon(float(fs[3][:-1]) / 10000)
            z_angle = deg_to_gon(float(fs[4][:-3]) / 10000)
            p = PolarPoint(angle_unit='gon',
                           z_angle_type='z',
                           dist_type='s',
                           dist=dist,
                           angle=angle,
                           z_angle=z_angle,
                           th=th,
                           base_point=bp,
                           pid=pid,
                           text=text,
                           coordorder=coordorder)
            f = Feature(p.to_point(),
                        desc=text,
                        id=pid)
            points.append(f)
        logger.debug(points)
        return points
