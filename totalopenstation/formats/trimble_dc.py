# -*- coding: utf-8 -*-
# filename: formats/trimble_dc.py
# Copyright 2021 Enzo Cocca <enzo.ccc@gmail.com>

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

"""Trimble DC format parser.

This format is used by Trimble data collectors. It uses fixed-width
fields with a record type identifier at the beginning of each line.

Record types:
    69TM - Measurement record containing coordinates

Field positions for 69TM records:
    [0:4]   - Record type (69TM)
    [4:20]  - Point ID
    [20:36] - Northing (Y)
    [36:51] - Easting (X)
    [51:68] - Elevation (Z)
    [68:84] - Description
"""

import logging

from . import Feature, Parser, Point

logger = logging.getLogger(__name__)


class FormatParser(Parser):
    """Parser for Trimble DC format.

    Args:
        data (str): A string containing the raw data to parse.
    """

    def is_point(self, line):
        """Check if a line contains point data.

        Returns:
            bool: True if the line is a 69TM measurement record.
        """
        return line.startswith('69TM')

    def get_point(self, line):
        """Extract point data from a 69TM record.

        Args:
            line (str): A line of text containing point data.

        Returns:
            Feature: A Feature object with the point geometry.
        """
        try:
            # Parse fixed-width fields
            point_id = line[4:20].strip()
            y = float(line[20:36])   # Northing
            x = float(line[36:51])   # Easting
            z = float(line[51:68])   # Elevation
            desc = line[68:84].strip() if len(line) > 68 else ''

            point = Point(x, y, z)
            feature = Feature(point, desc=desc, id=point_id, point_name=point_id)
            return feature
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse line: {line}. Error: {e}")
            return None
