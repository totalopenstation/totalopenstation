#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2008, 2009, 2011 Stefano Costa <steko@iosa.it>
# Copyright 2016 Damien Gaignon <damien.gaignon@gmail.com>
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
import cStringIO


class OutputFormat:

    """
    Exports points data in CSV format.

    ``data`` should be an iterable containing Feature objects.
    """

    def __init__(self, data):
        self.data = data
        self.output = cStringIO.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_NONNUMERIC)

    def process(self):
        rows = []
        try:
            self.data[0].geometry.z
        except ValueError:
            self.writer.writerow(('PID', 'type', 'Point Name', 'x', 'y', 'angle', 'z_angle', 'distance',
                                 'th', 'ih', 'circle', 'station'))
        else:
            self.writer.writerow(('PID', 'type', 'Point Name', 'x', 'y', 'z', 'angle', 'z_angle', 'distance',
                                  'th', 'ih', 'circle', 'station'))
        for feature in self.data:
            row = [feature.id,
                   feature.desc,
                   feature.point_name,
                   feature.geometry.x,
                   feature.geometry.y]
            try:
                row.append(feature.geometry.z)
            except ValueError:
                pass
            if feature.desc == "PT":
                row.extend([""] * 6)
            if feature.desc == "ST":
                row.extend([""] * 4)
                try:
                    row.extend([feature.properties["ih"],
                               ""])
                except KeyError:
                    row.extend([""] * 2)
            if feature.desc == "BS":
                row.extend([""] * 5)
                row.extend([feature.properties["circle"]])
            if feature.desc == "PO":
                try:
                    feature.properties["azimuth"]
                except KeyError:
                    pass
                else:
                    angle = feature.properties["azimuth"]
                if feature.properties["angle"] is not None:
                    angle = feature.properties["angle"]

                if feature.properties["slope_dist"] is not None:
                    dist = feature.properties["slope_dist"]
                elif feature.properties["horizontal_dist"] is not None:
                    dist = feature.properties["horizontal_dist"]
                row.extend([angle,
                           feature.properties["z_angle"],
                           dist,
                           feature.properties["th"]])
                row.extend([""] * 2)
                try:
                    row.extend([feature.properties["st_name"]])
                except KeyError:
                    row.extend([""])
            self.writer.writerow(row)

        return self.output.getvalue()
