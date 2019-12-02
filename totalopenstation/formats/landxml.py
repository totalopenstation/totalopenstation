#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: landxml.py
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

import xml.etree.ElementTree as xml

from . import Parser


class Survey:
    """
    Populate the survey tag of LandXML.

    Tags should be in order (convention):
        - SurveyHeader
        - Equipment
        - CgPoints
        - InstrumentSetup0
        - InstrumentSetupX
        - ObservationGroup0
        - ObservationGroupX

    """

    def __init__(self):
        """
        Initialize the Survey header tag
        """
        self.survey = xml.Element("Survey")
        xml.SubElement(self.survey, "SurveyHeader",
                       name="from TOPS")
        self.id = 0

    def _tag_position(self, tag):
        tags = ("SurveyHeader", "Equipment", "CgPoints", "InstrumentSetup")
        pos = 0

        for index in range(tags.index(tag)):
            if self.survey.find("./%s" % tags[index]) is not None:
                pos += 1
            else:
                pos = 1

        if tag == "InstrumentSetup":
            pos += len(self.survey.findall("./InstrumentSetup"))

        return pos



    def setup(self, **kwargs):
        """
        Populate the InstrumentSetup and ObservationGroup tags.

        InstrumentSetup is not a mandatory tag.

        Some attributes are mandatory but can be empty (so kwargs can be empty).

        Arguments in kwargs for InstrumentSetup (attrib mandatory as attrib*):
            - point_name -> stationName      attrib* of InstrumentSetup
            - ih         -> instrumentHeight attrib* of InstrumentSetup
            - pid        -> pntRef           attrib  of InstrumentPoint part of InstrumentSetup
            - instru_x   -> x coordinate     element of InstrumentPoint part of InstrumentSetup
            - instru_y   -> y coordinate     element of InstrumentPoint part of InstrumentSetup
            - instru_z   -> z coordinate     element of InstrumentPoint part of InstrumentSetup
            - attrib     -> attribX          attrib  of Property part of Feature

        Arguments in kwargs for Observationgroup (attrib mandatory as attrib*):
            - circle    -> azimuth          attrib* of Backsight part of ObservationGroup
            - back_name -> name             attrib  of BacksightPoint part of Backsight
            - back_x    -> x coordinate     element of BacksightPoint part of Backsight
            - back_y    -> y coordinate     element of BacksightPoint part of Backsight
            - back_z    -> z coordinate     element of BacksightPoint part of Backsight
        """

        # kwargs = {key: str(value) if value is not None else value for key,value in kwargs.items()}
        # Verification of position of the element
        pos = self._tag_position('InstrumentSetup')

        # Creation of InstrumentSetup tag, subelement of Survey
        instrument_setup = xml.Element("InstrumentSetup",
                                       id="setup" + str(self.id),
                                       stationName="",
                                       instrumentHeight="")
        # Fill of InstrumentSetup attributes
        if "point_name" in kwargs:
            instrument_setup.set("stationName", str(kwargs["point_name"]))
        if "ih" in kwargs:
            instrument_setup.set("instrumentHeight", str(kwargs["ih"]))
        if "hz0" in kwargs:
            instrument_setup.set("orientationAzimuth", str(kwargs["hz0"]))
        # attrib is not mandatory in InstrumentSetup so this is a feature
        if "attrib" in kwargs and kwargs["attrib"]:
            if instrument_setup.find("./Feature") is None:
                feature = xml.SubElement(instrument_setup, "Feature")
            # feature_property
            for i in range(len(kwargs["attrib"])):
                xml.SubElement(feature, "Property",
                               label="attrib%s" % (i + 1),
                               value=str(kwargs["attrib"][i]))

        # Creation of InstrumentPoint tag, subelement of InstrumentSetup
        instrument_point = xml.SubElement(instrument_setup, "InstrumentPoint")
        # Fill of InstrumentPoint attributes
        if "pid" in kwargs:
            instrument_point.set("pntRef", str(kwargs["pid"]))
        if "instru_x" in kwargs:
            instrument_point.text = "%s %s %s" % (str(kwargs["instru_x"]),
                                                  str(kwargs["instru_y"]),
                                                  str(kwargs["instru_z"]))
        # instrument_setup.append(instrument_point)
        self.survey.insert(pos, instrument_setup)

        # Creation of ObservationGroup tag, subelement of Survey
        observation_group = xml.Element("ObservationGroup",
                                        id="o" + str(self.id))
        # Creation of Backsight tag, subelement of ObservationGroup
        if "circle" in kwargs or "back_x" in kwargs:
            backsight = xml.SubElement(observation_group, "Backsight",
                                       circle="0.",
                                       setupID="setup" + str(self.id))
            # Fill of Backsight attributes
            if "circle" in kwargs:
                backsight.set("circle", str(kwargs["circle"]))
            if "back_x" in kwargs:
                # Creation of BacksightPoint tag, subelement of Backsight
                backsight_point = xml.SubElement(backsight, "BacksightPoint")
                # Fill of BacksightPoint attributes
                if "back_name" in kwargs:
                    backsight_point.set("name", str(kwargs["back_name"]))
                if "back_x" in kwargs:
                    backsight_point.text = "%s %s %s" % (str(kwargs["back_x"]),
                                                         str(kwargs["back_y"]),
                                                         str(kwargs["back_z"]))
        # backsight.append(backsight_point)
        # observation_group.append(backsight)
        self.survey.insert(pos * 2, observation_group)

        # ID can be raise
        self.id += 1

    def to_string(self):
        """
        :return:
        """
        return xml.tostring(self.survey)

