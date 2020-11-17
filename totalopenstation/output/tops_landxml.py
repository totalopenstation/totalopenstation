#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_landxml.py
# Copyright 2015 Damien Gaignon <damien.gaignon@gmail.com>
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

from totalopenstation.formats.landxml import Survey, LandXML
from . import Builder

class OutputFormat(Builder):

    """
    Exports points data in LandXML format.

    ``data`` should be an iterable containing Feature objects.

    This is consistent with our current standard.
    """

    def __init__(self, data):
        self.data = data

    def _get_feature(self, feature):
        kwargs = {}
        kwargs["x"] = feature.geometry.x
        kwargs["y"] = feature.geometry.y
        try:
            kwargs["z"] = feature.geometry.z
        except ValueError:
            pass

        for key,value in feature.properties.items():
            kwargs[key] = value

        return kwargs

    def process(self):

        root = Survey()

        for feature in self.data:
            kwargs = self._get_feature(feature)

            if feature.desc == "PO":
                root.raw_observation(**kwargs)
            if feature.desc == "PT":
                root.cg_point(**kwargs)
            if feature.desc == "ST":
                root.setup(**kwargs)

        xml = LandXML()
        xml.append(root.survey)

        return xml.to_string()
