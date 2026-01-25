# -*- coding: utf-8 -*-
# filename: formats/detect.py
# Copyright 2025 Enzo Cocca <enzo.ccc@gmail.com>

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

"""Auto-detection of survey data file formats.

This module provides functionality to automatically detect the format
of survey data files based on their content patterns.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Format detection patterns
# Each format has a list of patterns that must match (necessary)
# and patterns where at least one must match (sufficient)
FORMAT_PATTERNS = {
    'landxml': {
        'necessary': [
            r'<LandXML',
        ],
        'sufficient': [
            r'xmlns.*landxml',
            r'<CgPoints',
            r'<Survey',
        ],
        'description': 'LandXML format (XML-based)',
    },
    'leica_gsi': {
        'necessary': [],
        'sufficient': [
            r'^\*?\d{6}\+\d+.*21\.\d{3}\+',  # GSI16 format
            r'^\d{6}\+\d+\s+21\.\d{3}\+',    # GSI8 format
        ],
        'description': 'Leica GSI format (8 or 16 character)',
    },
    'leica_tcr_1205': {
        'necessary': [],
        'sufficient': [
            r'Instrument:\s*TCR1205',
            r'TCR1205',
        ],
        'description': 'Leica TCR 1205 format',
    },
    'leica_tcr_705': {
        'necessary': [],
        'sufficient': [
            r'Instrument:\s*TCR705',
            r'TCR705',
        ],
        'description': 'Leica TCR 705 format',
    },
    'nikon_raw_v200': {
        'necessary': [],
        'sufficient': [
            r'CO,Nikon RAW data format',
            r'CO.*RAW.*V2\.00',
        ],
        'description': 'Nikon RAW V2.00 format',
    },
    'sokkia_sdr33': {
        'necessary': [],
        'sufficient': [
            r'^00NM.*SDR',
            r'^10NM.*JOB',
            r'^0[0-9]NM|^0[0-9]TP',
        ],
        'description': 'Sokkia SDR33 format',
    },
    'topcon_gts': {
        'necessary': [],
        'sufficient': [
            r'\+\d+m\d+\+\d+g\+',
            r'_\+\d+_.*\+\d+m\d+',
        ],
        'description': 'Topcon GTS format',
    },
    'carlson_rw5': {
        'necessary': [],
        'sufficient': [
            r'^--.*RW5',
            r'^JB,NM',
            r'^MO,AD\d',
            r'^OC,OP\d+',
            r'^SS,OP\d+',
        ],
        'description': 'Carlson RW5 format',
    },
    'trimble_are': {
        'necessary': [],
        'sufficient': [
            r'^0=',
            r'^\d+=.*,\d+=',
        ],
        'description': 'Trimble ARE format',
    },
    'zeiss_r5': {
        'necessary': [],
        'sufficient': [
            r'^\s+\d+\s+\d+\.\d{3,}',
            r'Rec\s+Hz\s+V\s+SD',
        ],
        'description': 'Zeiss R5 format',
    },
    'zeiss_rec_500': {
        'necessary': [],
        'sufficient': [
            r'^\s{0,3}\d{1,4}\s{2,}',
            r'END\s*$',
        ],
        'description': 'Zeiss REC 500 format',
    },
}

# TOPS format marker (for pre-tagged files)
TOPS_FORMAT_MARKER = r'#\s*-\*-\s*tops-format:\s*(\w+)\s*-\*-'


def detect_format(data, return_all=False):
    """Detect the format of survey data.

    Args:
        data (str): The raw data string to analyze.
        return_all (bool): If True, return all matching formats with scores.
                          If False, return only the best match.

    Returns:
        str or list: The detected format name (key from BUILTIN_INPUT_FORMATS),
                     or None if no format could be detected.
                     If return_all=True, returns a list of (format_name, score) tuples.
    """
    # First, check for TOPS format marker
    marker_match = re.search(TOPS_FORMAT_MARKER, data[:500])
    if marker_match:
        format_name = marker_match.group(1)
        logger.info(f"Found TOPS format marker: {format_name}")
        if return_all:
            return [(format_name, 100)]
        return format_name

    # Analyze the data for each format
    matches = []

    for format_name, patterns in FORMAT_PATTERNS.items():
        score = _calculate_match_score(data, patterns)
        if score > 0:
            matches.append((format_name, score))
            logger.debug(f"Format {format_name} matched with score {score}")

    if not matches:
        logger.warning("Could not detect data format automatically")
        if return_all:
            return []
        return None

    # Sort by score (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)

    if return_all:
        return matches

    best_match = matches[0][0]
    logger.info(f"Detected format: {best_match} (score: {matches[0][1]})")
    return best_match


def _calculate_match_score(data, patterns):
    """Calculate how well the data matches a format's patterns.

    Args:
        data (str): The raw data string.
        patterns (dict): Dictionary with 'necessary' and 'sufficient' pattern lists.

    Returns:
        int: Match score (0 if necessary conditions not met).
    """
    necessary = patterns.get('necessary', [])
    sufficient = patterns.get('sufficient', [])

    # Check necessary conditions (all must match)
    for pattern in necessary:
        if not re.search(pattern, data, re.MULTILINE | re.IGNORECASE):
            return 0

    # Count sufficient conditions (at least one should match)
    score = len(necessary) * 10  # Base score for meeting necessary conditions

    sufficient_matches = 0
    for pattern in sufficient:
        if re.search(pattern, data, re.MULTILINE | re.IGNORECASE):
            sufficient_matches += 1
            score += 5

    # If no necessary patterns but no sufficient matches either, return 0
    if not necessary and sufficient_matches == 0:
        return 0

    return score


def get_format_description(format_name):
    """Get a human-readable description of a format.

    Args:
        format_name (str): The format identifier.

    Returns:
        str: A description of the format, or None if not found.
    """
    if format_name in FORMAT_PATTERNS:
        return FORMAT_PATTERNS[format_name].get('description', format_name)
    return None


def list_detectable_formats():
    """List all formats that can be auto-detected.

    Returns:
        list: List of (format_name, description) tuples.
    """
    return [(name, patterns.get('description', name))
            for name, patterns in FORMAT_PATTERNS.items()]
