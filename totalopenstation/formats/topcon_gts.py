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
import re

from .polar import BasePoint, PolarPoint
from totalopenstation.formats.conversion import deg_to_gon
from . import Feature

logger = logging.getLogger(__name__)


class FormatParser:
    '''A FormatParser for Topcon GTS polar format.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.

    This parser handles two data formats:
    1. Serial-downloaded data with artifacts (prefix/suffix characters on each line)
    2. Clean exported data without artifacts
    '''

    def __init__(self, data):
        self.raw_data = data
        self.rows = []
        self.parse_errors = []

        # Try to detect and parse the data format
        self._parse_data(data)

        logger.info(f"Topcon GTS parser initialized with {len(self.rows)} data rows")
        if not self.rows:
            logger.warning("No data rows found. Check if the file format is correct.")
            logger.debug(f"Raw data preview (first 500 chars): {data[:500]}")

    def _parse_data(self, data):
        '''Try different parsing strategies to extract data rows.'''

        lines = data.splitlines()
        logger.debug(f"Input has {len(lines)} lines")

        # Strategy 1: Serial-downloaded data with artifacts
        # Each line has a prefix char and 4-digit suffix + newline artifacts
        if self._try_serial_format(lines):
            logger.info("Detected serial-downloaded format with artifacts")
            return

        # Strategy 2: Clean data (no artifacts)
        if self._try_clean_format(data):
            logger.info("Detected clean data format")
            return

        # Strategy 3: Try to find comma-separated measurement blocks
        if self._try_flexible_format(data):
            logger.info("Detected flexible format with comma separators")
            return

        logger.warning("Could not detect data format. No rows extracted.")

    def _try_serial_format(self, lines):
        '''Parse serial-downloaded data with line artifacts.

        Expected format: each line starts with a control char and ends with
        4 digits that are part of a checksum or line number.
        '''
        try:
            # Check if lines have the expected artifact pattern
            valid_lines = [l for l in lines if len(l) >= 6]
            if not valid_lines:
                return False

            # Original parsing: remove first char and last 5 chars from each line
            clean_data = ''.join([l[1:-5] for l in lines if len(l) > 6])

            if not clean_data:
                return False

            rows = clean_data.split(',')
            # Validate that we got measurement-like data (should contain '+' separators)
            valid_rows = [r for r in rows if '+' in r and len(r) > 10]

            if valid_rows:
                self.rows = rows
                logger.debug(f"Serial format: extracted {len(self.rows)} rows")
                return True

        except Exception as e:
            logger.debug(f"Serial format parsing failed: {e}")

        return False

    def _try_clean_format(self, data):
        '''Parse clean exported data without line artifacts.'''
        try:
            # Try splitting directly on commas
            rows = data.replace('\n', '').replace('\r', '').split(',')
            valid_rows = [r for r in rows if '+' in r and len(r) > 10]

            if valid_rows:
                self.rows = rows
                logger.debug(f"Clean format: extracted {len(self.rows)} rows")
                return True

        except Exception as e:
            logger.debug(f"Clean format parsing failed: {e}")

        return False

    def _try_flexible_format(self, data):
        '''Try to find measurement patterns using regex.'''
        try:
            # Look for patterns like: 1.500_+1_ ?+00043575m0968990+1360970g+00064625t
            pattern = r'[\d.]+_\+\d+_[^,]+'
            matches = re.findall(pattern, data)

            if matches:
                self.rows = matches
                logger.debug(f"Flexible format: extracted {len(self.rows)} rows")
                return True

        except Exception as e:
            logger.debug(f"Flexible format parsing failed: {e}")

        return False

    def _parse_row(self, row):
        '''Parse a single measurement row and return a Feature or None.'''
        fs = row.split('+')

        if len(fs) < 5:
            logger.debug(f"Row has insufficient fields ({len(fs)}): {row[:50]}...")
            return None

        try:
            pid = fs[1][:-3] if len(fs[1]) > 3 else fs[1]
        except IndexError:
            logger.debug(f"Could not extract point ID from row: {row[:50]}...")
            return None

        try:
            text = fs[-1][0:5] if len(fs[-1]) >= 5 else fs[-1]
        except IndexError:
            text = ''

        try:
            th_str = fs[0][:-1] if fs[0] else '0'
            th = float(th_str) if th_str else 0.0
        except (ValueError, IndexError) as e:
            logger.debug(f"Could not parse target height from '{fs[0]}': {e}")
            return None

        try:
            dist_str = fs[2].split('m')[0] if 'm' in fs[2] else fs[2]
            dist = float(dist_str)
        except (ValueError, IndexError) as e:
            logger.debug(f"Could not parse distance from '{fs[2] if len(fs) > 2 else 'N/A'}': {e}")
            return None

        try:
            angle_str = fs[3][:-1] if len(fs[3]) > 1 else fs[3]
            angle = deg_to_gon(float(angle_str) / 10000)
        except (ValueError, IndexError) as e:
            logger.debug(f"Could not parse angle from '{fs[3] if len(fs) > 3 else 'N/A'}': {e}")
            return None

        try:
            z_angle_str = fs[4][:-3] if len(fs[4]) > 3 else fs[4]
            z_angle = deg_to_gon(float(z_angle_str) / 10000)
        except (ValueError, IndexError) as e:
            logger.debug(f"Could not parse z_angle from '{fs[4] if len(fs) > 4 else 'N/A'}': {e}")
            return None

        bp = BasePoint(x=0, y=0, z=0, ih=0, b_zero_st=0.0)
        coordorder = 'NEZ'

        try:
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
            return f
        except Exception as e:
            logger.debug(f"Could not create Feature for point {pid}: {e}")
            return None

    @property
    def points(self):
        points = []
        errors = 0

        for i, row in enumerate(self.rows):
            feature = self._parse_row(row)
            if feature:
                points.append(feature)
            else:
                errors += 1

        if errors > 0:
            logger.info(f"Parsed {len(points)} points, {errors} rows could not be parsed")

        if not points and self.rows:
            logger.warning(
                f"No points could be extracted from {len(self.rows)} data rows. "
                "The data format may not match the expected Topcon GTS format. "
                "Try using a different format parser (e.g., topcon_ascii, topcon_gt7)."
            )
        elif not points:
            logger.warning(
                "No points found. The file may be empty or in an unsupported format. "
                "Please check if you selected the correct input format."
            )

        logger.debug(f"Returning {len(points)} points")
        return points
