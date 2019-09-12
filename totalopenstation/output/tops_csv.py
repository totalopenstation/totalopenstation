#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2019 Stefano Costa <steko@iosa.it>
# Copyright 2019 Damien Gaignon <damien.gaignon@gmail.com>
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

import csv
import io


class OutputFormat:

    """
    Exports points data in CSV format.

    ``data`` should be an iterable containing Feature objects.
    """

    def __init__(self, data):
        self.data = data
        self.output = io.StringIO()
        fieldnames = ['pid', 'type', 'point_name', 'x', 'y', 'z', 'angle', 'z_angle', 'distance',
                      'th', 'ih', 'circle', 'station']
        self.writer = csv.DictWriter(self.output, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
        self.writer.writeheader()

    def process(self):

        def value_or_empty(property_name):
            try:
                value = feature.properties[property_name]
            except KeyError:
                value = ''
            return value

        for feature in self.data:
            row = {
                'pid': feature.id,
                'type': feature.desc,
                'x' : feature.geometry.x,
                'y': feature.geometry.y
            }

            try:  # not all input formats include z coordinates
                row['z'] = feature.geometry.z
            except ValueError:
                row['z'] = ''

            # a few cases with simple yes/no logic
            for p in ['point_name', 'ih', 'circle', 'z_angle', 'th']:
                row[p] = feature.properties[p] if p in feature.properties else ''

            try:  # not all input formats include azimuth/angle
                row['angle'] = feature.properties['azimuth']
            except KeyError:
                try:
                    row['angle'] = feature.properties['angle']
                except KeyError:
                    row['angle'] = ''

            try:  # not all input formats include distance
                row['dist'] = feature.properties['slope_dist']
            except KeyError:
                try:
                    row['distance'] = feature.properties['horizontal_dist']
                except KeyError:
                    row['distance'] = ''

            try:  # not all input formats include station name
                row['station'] = feature.properties['st_name']
            except KeyError:
                row['station'] = ''

            self.writer.writerow(row)

        return self.output.getvalue()
