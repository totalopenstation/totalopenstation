# -*- coding: utf-8 -*-
# filename: tops_kml.py
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

"""KML output format for Total Open Station.

This module exports survey data to KML (Keyhole Markup Language) format,
which can be opened in Google Earth, QGIS, and other GIS applications.

Note: KML uses geographic coordinates (longitude, latitude, altitude in WGS84).
Survey data is typically in local/projected coordinates, so the exported KML
may need coordinate transformation for proper display on a map.
"""

import simplekml

from . import Builder


class OutputFormat(Builder):
    """Exports points data in KML format.

    KML (Keyhole Markup Language) is an XML-based format for geographic
    data visualization in applications like Google Earth.

    ``data`` should be an iterable containing Feature objects with
    Point or LineString geometries.
    """

    def __init__(self, data):
        self.data = data

    def process(self):
        """Process the input data and return a KML string.

        Returns:
            str: A KML document as a string.
        """
        kml = simplekml.Kml(name="Total Open Station Export")

        # Group features by description for folder organization
        folders = {}

        for feature in self.data:
            geom = feature.geometry
            desc = feature.desc or "Unknown"

            # Create folder for each description if not exists
            if desc not in folders:
                folders[desc] = kml.newfolder(name=desc)

            folder = folders[desc]

            if geom.geom_type == 'Point':
                self._add_point(folder, feature, geom)
            elif geom.geom_type == 'LineString':
                self._add_linestring(folder, feature, geom)

        return kml.kml()

    def _add_point(self, folder, feature, geom):
        """Add a Point feature to the KML folder."""
        try:
            coords = (float(geom.x), float(geom.y), float(geom.z))
        except (ValueError, AttributeError):
            coords = (float(geom.x), float(geom.y))

        point = folder.newpoint(
            name=str(feature.id),
            description=feature.desc or "",
            coords=[coords]
        )

        # Add extended data for properties
        if hasattr(feature, 'properties') and feature.properties:
            for key, value in feature.properties.items():
                point.extendeddata.newdata(name=key, value=str(value))

    def _add_linestring(self, folder, feature, geom):
        """Add a LineString feature to the KML folder."""
        coords = []
        for coord in geom.coords:
            if len(coord) >= 3:
                coords.append((coord[0], coord[1], coord[2]))
            else:
                coords.append((coord[0], coord[1]))

        linestring = folder.newlinestring(
            name=str(feature.id),
            description=feature.desc or "",
            coords=coords
        )
