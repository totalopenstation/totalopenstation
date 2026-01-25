# -*- coding: utf-8 -*-
# filename: formats/topcon_gpt.py
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

"""Topcon GPT format parser.

This format is used by Topcon GPT series total stations.
Lines containing 'SD' (shot data) are parsed as point records.

Format: point_id,SD,northing,easting,elevation
"""

import logging

from . import Feature, Parser, Point

logger = logging.getLogger(__name__)


class FormatParser(Parser):
    """Parser for Topcon GPT format.

    Args:
        data (str): A string containing the raw data to parse.
    """

    def is_point(self, line):
        """Check if a line contains point data.

        Returns:
            bool: True if the line contains 'SD' (shot data).
        """
        return 'SD' in line

    def get_point(self, line):
        """Extract point data from a line.

        Args:
            line (str): A line of text containing point data.

        Returns:
            Feature: A Feature object with the point geometry.
        """
        try:
            parts = line.strip().split(',')
            point_id = parts[0].strip()
            # SD is in parts[1]
            y = float(parts[2])   # Northing
            x = float(parts[3])   # Easting
            z = float(parts[4])   # Elevation

            point = Point(x, y, z)
            feature = Feature(point, desc=point_id, id=point_id)
            return feature
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse line: {line}. Error: {e}")
            return None
