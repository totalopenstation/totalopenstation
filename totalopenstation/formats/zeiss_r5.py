## -*- coding: utf-8 -*-
# filename: formats/zeiss_r5.py
# Copyright 2015 Stefano Costa <steko@iosa.it>

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

from . import Feature, Point

logger = logging.getLogger(__name__)


class FormatParser:

    def __init__(self, data):
        self.rows = (r for r in data.splitlines())

    @property
    def points(self):
        '''Point features.'''

        points = []

        def record(recstr):
            fields = recstr.split('|')
            record_fields = {}
            adr, reco, coords = fields[1], fields[2], fields[3:6]
            record_fields['Adr'] = adr.split()[1].strip()
            record_fields['type'] = reco[0:2]
            if record_fields['type'] == 'KR':
                record_fields['id'] = reco[6:10]
                record_fields['desc'] = reco[3:6]
                for xyz in coords:
                    coord = xyz[0]
                    value = xyz[1:].strip()
                    if value.endswith(' m'):
                        value = value[0:-2]
                    if len(value) > 2:
                        record_fields[coord] = value
            elif record_fields['type'] == 'TR':
                record_fields['desc'] = reco[3:10]
            logger.info("record_fields : %s" % (record_fields))
            return record_fields

        for row in self.rows:
            if row.startswith('END'):
                break
            else:
                rec = record(row)
                if rec['type'] == 'KR':
                    try:
                        point = Point(rec['X'],
                                      rec['Y'],
                                      rec['Z'])
                    except KeyError:
                        try:
                            point = Point(rec['X'],
                                          rec['Y'])
                        except KeyError:
                            continue
                    finally:
                        feature = Feature(point,
                                          desc=rec['desc'],
                                          id=rec['id'])
                        points.append(feature)
        logger.debug(points)
        return points
