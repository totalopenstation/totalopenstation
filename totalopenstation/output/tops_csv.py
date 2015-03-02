#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2008, 2009, 2011 Stefano Costa <steko@iosa.it>
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

    ``data`` should be an iterable (e.g. list) containing one iterable
    (e.g.  tuple) for each point. The default order is PID, x, x, z,
    TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data):
        self.data = data
        self.output = cStringIO.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_NONNUMERIC)

    def process(self):
        self.writer.writerow(('PID', 'x', 'y', 'z', 'TEXT'))
        self.writer.writerows(self.data)
        return self.output.getvalue()
