#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2019 Stefano Costa <steko@iosa.it>
# Copyright 2019 Damien Gaignon <damien.gaignon@gmail.com>
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
import io

from . import Builder, OutputOption


class OutputFormat(Builder):

    """
    Exports points data in CSV format.

    ``data`` should be an iterable containing Feature objects.

    Options:
        separator: Field separator character (default: ',')
        include_z: Include Z coordinates (default: True)
        include_header: Include header row (default: True)
    """

    OPTIONS = [
        OutputOption(
            name='separator',
            label='Field Separator',
            option_type='choice',
            default=',',
            choices=[',', ';', '\t', '|'],
            description='Character used to separate fields'
        ),
        OutputOption(
            name='include_z',
            label='Include Z Coordinates',
            option_type='bool',
            default=True,
            description='Include elevation/Z values in output'
        ),
        OutputOption(
            name='include_header',
            label='Include Header Row',
            option_type='bool',
            default=True,
            description='Include column names as first row'
        ),
    ]

    def __init__(self, data, **options):
        super().__init__(data, **options)
        self.output = io.StringIO()

        # Build fieldnames based on options
        fieldnames = ['pid', 'type', 'point_name', 'x', 'y']
        if self.get_option('include_z'):
            fieldnames.append('z')
        fieldnames.extend(['angle', 'z_angle', 'distance', 'th', 'ih', 'circle', 'station'])

        self.fieldnames = fieldnames
        separator = self.get_option('separator') or ','

        # Use custom delimiter
        self.writer = csv.DictWriter(
            self.output,
            quoting=csv.QUOTE_NONNUMERIC,
            fieldnames=fieldnames,
            delimiter=separator
        )

        if self.get_option('include_header'):
            self.writer.writeheader()

    def process(self):

        for feature in self.data:
            row = {
                'pid': feature.id,
                'type': feature.desc,
                'x' : feature.geometry.x,
                'y': feature.geometry.y
            }

            if self.get_option('include_z'):
                try:  # not all input formats include z coordinates
                    row['z'] = feature.geometry.z
                except ValueError:
                    row['z'] = ''

            # a few cases with simple yes/no logic
            for prop in ['point_name', 'ih', 'circle', 'z_angle', 'th']:
                row[prop] = feature.properties.get(prop, '')  # empty string as default value

            # not all input formats include azimuth/angle
            row['angle'] = feature.properties.get('azimuth',
                                                  feature.properties.get('angle', ''))

            # not all input formats include distance
            row['distance'] = feature.properties.get('slope_dist',
                                                 feature.properties.get('horizontal_dist', ''))

            # not all input formats include station name
            row['station'] = feature.properties.get('st_name', '')

            self.writer.writerow(row)

        return self.output.getvalue()

class TrimbleOutputFormat(OutputFormat):
    """
    Exports points data in Trimble CSV format,
    used for LandSurveyCodesImport QGIS plugin.

    ``data`` should be an iterable containing Feature objects.
    """

    def __init__(self, data):
        self.data = data
        self.output = io.StringIO()
        fieldnames = [
            "id",
            "x",
            "y",
            "z",
            "type",
            "point_name",
            "angle",
            "z_angle",
            "distance",
            "th",
            "ih",
            "circle",
            "station",
        ]
        self.writer = csv.DictWriter(
            self.output, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames
        )
        self.writer.writeheader()

    def process(self):

        for feature in self.data:
            row = {
                "id": feature.id,
                "type": feature.desc,
                "x": feature.geometry.x,
                "y": feature.geometry.y,
            }

            try:  # not all input formats include z coordinates
                row["z"] = feature.geometry.z
            except ValueError:
                row["z"] = ""

            # a few cases with simple yes/no logic
            for prop in ["point_name", "ih", "circle", "z_angle", "th"]:
                row[prop] = feature.properties.get(
                    prop, ""
                )  # empty string as default value

            # not all input formats include azimuth/angle
            row["angle"] = feature.properties.get(
                "azimuth", feature.properties.get("angle", "")
            )

            # not all input formats include distance
            row["distance"] = feature.properties.get(
                "slope_dist", feature.properties.get("horizontal_dist", "")
            )

            # not all input formats include station name
            row["station"] = feature.properties.get("st_name", "")

            self.writer.writerow(row)

        return self.output.getvalue()
