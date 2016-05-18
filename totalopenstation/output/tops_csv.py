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
        try:
            self.data[0].geometry.z
        except ValueError:
            self.writer.writerow(('PID', 'x', 'y', 'TEXT'))
            self.writer.writerows((feature.id,
                                   feature.geometry.x,
                                   feature.geometry.y,
                                   feature.desc) for feature in self.data)
        else:
            self.writer.writerow(('PID', 'x', 'y', 'z', 'TEXT'))
            self.writer.writerows((feature.id,
                                   feature.geometry.x,
                                   feature.geometry.y,
                                   feature.geometry.z,
                                   feature.desc) for feature in self.data)
        return self.output.getvalue()
