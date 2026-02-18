# -*- coding: utf-8 -*-
# filename: formats/trimble_jxl.py
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

"""Trimble JobXML (JXL) format parser.

This format is used by Trimble total stations and data collectors
including Trimble C3, C5, M3, S series, and others running
Trimble Access or Trimble General Survey software.

The JXL format is XML-based and contains:
- PointRecord elements with Grid or ComputedGrid coordinates
- StationRecord for station setups
- Circle elements with polar observations (Hz, V, distance)
- Metadata about instrument, atmosphere, corrections, etc.

Coordinate order in JXL is typically North-East-Elevation.
"""

import logging
import xml.etree.ElementTree as ET

from . import Feature, Parser, Point

logger = logging.getLogger(__name__)


class FormatParser(Parser):
    """Parser for Trimble JobXML (JXL) format.

    Args:
        data (str): A string containing the raw XML data to parse.
    """

    def __init__(self, data):
        self.data = data
        self._points = None
        self._root = None
        self._coord_order = 'NEZ'  # Default: North-East-Elevation

        try:
            self._root = ET.fromstring(data)
            self._detect_coord_order()
        except ET.ParseError as e:
            logger.error(f"Failed to parse XML: {e}")
            self._root = None

    def _detect_coord_order(self):
        """Detect coordinate order from UnitsRecord."""
        if self._root is None:
            return

        # Find UnitsRecord to determine coordinate order
        for units in self._root.iter('UnitsRecord'):
            coord_order = units.find('CoordinateOrder')
            if coord_order is not None and coord_order.text:
                order_text = coord_order.text.lower()
                if 'east' in order_text and 'north' in order_text:
                    if order_text.index('east') < order_text.index('north'):
                        self._coord_order = 'ENZ'
                    else:
                        self._coord_order = 'NEZ'
                logger.debug(f"Detected coordinate order: {self._coord_order}")
                break

    def is_point(self, element):
        """Check if an XML element is a valid point record.

        Args:
            element: An XML Element object.

        Returns:
            bool: True if the element contains usable coordinate data.
        """
        if element.tag != 'PointRecord':
            return False

        # Check if deleted
        deleted = element.find('Deleted')
        if deleted is not None and deleted.text == 'true':
            return False

        # Must have either Grid or ComputedGrid coordinates
        grid = element.find('Grid')
        computed_grid = element.find('ComputedGrid')

        if grid is not None:
            north = grid.find('North')
            east = grid.find('East')
            if north is not None and east is not None:
                return True

        if computed_grid is not None:
            north = computed_grid.find('North')
            east = computed_grid.find('East')
            if north is not None and east is not None:
                return True

        return False

    def get_point(self, element):
        """Extract point data from a PointRecord element.

        Args:
            element: An XML Element containing point data.

        Returns:
            Feature: A Feature object with the point geometry, or None.
        """
        try:
            # Get point name/ID
            name_elem = element.find('Name')
            point_name = name_elem.text if name_elem is not None else ''

            # Get code/description
            code_elem = element.find('Code')
            code = code_elem.text if code_elem is not None and code_elem.text else ''

            # Get classification (BackSight, Normal, etc.)
            class_elem = element.find('Classification')
            classification = class_elem.text if class_elem is not None else ''

            # Prefer ComputedGrid over Grid (computed has corrections applied)
            grid = element.find('ComputedGrid')
            if grid is None:
                grid = element.find('Grid')

            if grid is None:
                logger.debug(f"No grid coordinates for point {point_name}")
                return None

            north_elem = grid.find('North')
            east_elem = grid.find('East')
            elev_elem = grid.find('Elevation')

            if north_elem is None or east_elem is None:
                logger.debug(f"Missing N/E coordinates for point {point_name}")
                return None

            north_value = float(north_elem.text)
            east_value = float(east_elem.text)
            elevation = float(elev_elem.text) if elev_elem is not None and elev_elem.text else 0.0

            # Trimble JXL coordinate handling:
            # When CoordinateOrder is "North-East-Elevation", Trimble stores:
            # - <North> tag: first coordinate (which is actually Easting/X in UTM)
            # - <East> tag: second coordinate (which is actually Northing/Y in UTM)
            # This is because "North-East" refers to display order, not coordinate meaning.
            #
            # For UTM coordinates in Italy (zone 32N/33N):
            # - Easting (X): ~300,000 - 700,000
            # - Northing (Y): ~4,000,000 - 5,000,000
            #
            # We detect and swap if values appear inverted
            if north_value < 1000000 and east_value > 1000000:
                # Values appear swapped: North tag has Easting, East tag has Northing
                x = north_value  # Easting from North tag
                y = east_value   # Northing from East tag
                logger.debug(f"Detected swapped coordinates, using North={north_value} as X, East={east_value} as Y")
            else:
                # Standard interpretation
                x = east_value   # Easting from East tag
                y = north_value  # Northing from North tag
            z = elevation

            point = Point(x, y, z)

            # Build description from code and classification
            desc = code
            if classification and classification not in ('Normal', ''):
                desc = f"{code} [{classification}]" if code else classification

            feature = Feature(point,
                              desc=desc,
                              id=point_name,
                              point_name=point_name)

            # Add extra properties
            feature.properties['classification'] = classification
            feature.properties['code'] = code

            # Extract polar data if available
            circle = element.find('Circle')
            if circle is not None:
                hz = circle.find('HorizontalCircle')
                v = circle.find('VerticalCircle')
                dist = circle.find('EDMDistance')
                face = circle.find('Face')

                if hz is not None and hz.text:
                    feature.properties['angle'] = float(hz.text)
                if v is not None and v.text:
                    feature.properties['z_angle'] = float(v.text)
                if dist is not None and dist.text:
                    feature.properties['slope_dist'] = float(dist.text)
                if face is not None and face.text:
                    feature.properties['face'] = face.text

            # Extract station reference if available
            station_id = element.find('StationID')
            if station_id is not None and station_id.text:
                feature.properties['station_id'] = station_id.text

            return feature

        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse point: {e}")
            return None

    def split_points(self):
        """Split XML data into PointRecord elements.

        Returns:
            list: List of PointRecord XML elements.
        """
        if self._root is None:
            return []

        # Find all PointRecord elements
        point_records = list(self._root.iter('PointRecord'))
        logger.info(f"Found {len(point_records)} PointRecord elements")
        return point_records

    @property
    def points(self):
        """Parse and return all valid points.

        Returns:
            list: List of Feature objects representing points.
        """
        if self._points is not None:
            return self._points

        self._points = []
        seen_points = {}  # Track points by name to handle duplicates

        for element in self.split_points():
            if not self.is_point(element):
                continue

            feature = self.get_point(element)
            if feature is None:
                continue

            # Handle duplicate point names - keep the last one (most recent)
            # or the one with ComputedGrid (has corrections applied)
            point_name = feature.id
            if point_name in seen_points:
                # Check if this is a better version (has ComputedGrid)
                has_computed = element.find('ComputedGrid') is not None
                if has_computed:
                    # Replace with this version
                    idx = seen_points[point_name]
                    self._points[idx] = feature
                # Otherwise keep the existing one
            else:
                seen_points[point_name] = len(self._points)
                self._points.append(feature)

        logger.info(f"Extracted {len(self._points)} unique points")
        return self._points

    def get_stations(self):
        """Extract station setup information.

        Returns:
            list: List of dictionaries with station data.
        """
        if self._root is None:
            return []

        stations = []
        for station in self._root.iter('StationRecord'):
            station_data = {}

            name = station.find('StationName')
            if name is not None:
                station_data['name'] = name.text

            ih = station.find('TheodoliteHeight')
            if ih is not None and ih.text:
                station_data['instrument_height'] = float(ih.text)

            station_type = station.find('StationType')
            if station_type is not None:
                station_data['type'] = station_type.text

            station_id = station.get('ID')
            if station_id:
                station_data['id'] = station_id

            if station_data:
                stations.append(station_data)

        return stations

    def get_job_info(self):
        """Extract job metadata.

        Returns:
            dict: Dictionary with job information.
        """
        if self._root is None:
            return {}

        info = {}

        # From root attributes
        info['job_name'] = self._root.get('jobName', '')
        info['product'] = self._root.get('product', '')
        info['product_version'] = self._root.get('productVersion', '')
        info['timestamp'] = self._root.get('TimeStamp', '')

        # From InstrumentRecord
        for instrument in self._root.iter('InstrumentRecord'):
            model = instrument.find('Model')
            serial = instrument.find('Serial')
            if model is not None:
                info['instrument_model'] = model.text
            if serial is not None:
                info['instrument_serial'] = serial.text
            break

        return info
