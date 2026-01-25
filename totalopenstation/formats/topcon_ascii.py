# -*- coding: utf-8 -*-
# filename: formats/topcon_ascii.py
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

"""Topcon ASCII format parser.

This format is a simple CSV-like text format exported from Topcon
total stations. Each line contains comma-separated values:
    point_id, northing(y), easting(x), elevation(z), description

Note: The coordinate order is Y,X,Z (Northing, Easting, Elevation).

Example:
    1,2000.000,1000.000,100.000,POINT1
    2,2001.500,1001.500,100.250,POINT2
"""

import logging

from . import Feature, Parser, Point

logger = logging.getLogger(__name__)


class FormatParser(Parser):
    """Parser for Topcon ASCII format.

    Args:
        data (str): A string containing the raw data to parse.
    """

    def is_point(self, line):
        """Check if a line contains point data.

        Returns:
            bool: True if the line contains valid point data.
        """
        line = line.strip()
        if not line:
            return False
        parts = line.split(',')
        # Need at least 4 fields: id, y, x, z
        if len(parts) < 4:
            return False
        # Check that coordinates are numeric
        try:
            float(parts[1])
            float(parts[2])
            float(parts[3])
            return True
        except (ValueError, IndexError):
            return False

    def get_point(self, line):
        """Extract point data from a line.

        Args:
            line (str): A line of text containing point data.

        Returns:
            Feature: A Feature object with the point geometry.
        """
        parts = line.strip().split(',')
        try:
            point_id = parts[0].strip()
            # Note: Topcon format uses Y,X,Z order (Northing, Easting, Elevation)
            y = float(parts[1])  # Northing
            x = float(parts[2])  # Easting
            z = float(parts[3])  # Elevation
            desc = parts[4].strip() if len(parts) > 4 else ''

            point = Point(x, y, z)
            feature = Feature(point, desc=desc, id=point_id, point_name=point_id)
            return feature
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse line: {line}. Error: {e}")
            return None
