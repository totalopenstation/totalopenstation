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
import time
import re
import os

# Template string
TEMPLATE = '''<?xml version=\"1.0\"?>
                <LandXML xmlns=\"http://www.landxml.org/schema/LandXML-1.1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.landxml.org/schema/LandXML-1.1 http://www.landxml.org/schema/LandXML-1.1/LandXML-1.1.xsd\" date=\"\" time=\"\" version=\"1.1\">
                    <Units>
                        <Metric areaUnit=\"squareMeter\" linearUnit=\"meter\" volumeUnit=\"cubicMeter\" temperatureUnit=\"celsius\" pressureUnit=\"milliBars\" angularUnit=\"grads\" directionUnit=\"grads\"></Metric>
                    </Units>
                    <Project name=\"Template\"></Project>
                    <Application name=\"TotalOpen Station\" desc=\"TOPS\" manufacturer=\"\" version=\"\" manufacturerURL=\"http://tops.iosa.it/\" timeStamp=\"\"></Application>
                </LandXML>'''

DEFAULT_NS = "http://www.landxml.org/schema/LandXML-1.1"
DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'


def _indent(elem, level=0):
    """
    A function to indent a XML Element for pretty printing
    :param elem: The element to parse
    :param level: The level of the element in the hierarchy
    :return: The element ready to be pretty printed
    """
    i = "\n" + (level + 1)*"\t"
    j = "\n" + level*"\t"
    count = 1
    if len(elem):
        if elem.text is None or elem.text.strip() is None:
            elem.text = i
        for subelem in elem:
            _indent(subelem, level+1)
            if subelem.tail is None or subelem.tail.strip() is None:
                subelem.tail = i
            elif re.match(r"\s", subelem.tail):
                subelem.tail = i
            count += 1
        if count == len(elem) + 1:
            subelem.tail = j
    return elem


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

    def equipment(self, **kwargs):
        """
        Populate the Equipment tag.

        No attribut is mandatory so kwargs can be empty.

        Arguments in kwargs for Equipment:
            TODO
        """
        # kwargs = {key: str(value) if value is not None else value for key,value in kwargs.items()}
        # Verification of position of the element
        pos = self._tag_position('Equipment')

        # Creation of Equipment tag, subelement of Survey
        equipment = xml.Element("Equipment")
        self.survey.insert(pos, equipment)

    def cg_point(self, **kwargs):
        """
        Populate the CgPoints and CgPoint tags.

        No attribut is mandatory so kwargs can be empty.

        Arguments in kwargs for CgPoint:
            - point_name -> name          attrib  of CgPoint part of CgPoints
            - pid        -> pntRef        attrib  of CgPoint part of CgPoints
            - x          -> x coordinate  element of CgPoint part of CgPoints
            - y          -> y coordinate  element of CgPoint part of CgPoints
            - z          -> z coordinate  element of CgPoint part of CgPoints
            - attrib     -> attribX       attrib  of Property part of Feature
        """

        # kwargs = {key: str(value) if value is not None else value for key,value in kwargs.items()}
        # Verification of position of the element
        pos = self._tag_position('CgPoints')

        # Creation of CgPoints tag, subelement of Survey if it does not exist
        cgpoints = self.survey.find("./CgPoints")
        if cgpoints is None:
            cgpoints = xml.Element("CgPoints")
            self.survey.insert(pos, cgpoints)

        # Creation of CgPoint tag, subelement of CgPoints
        cgpoint = xml.SubElement(cgpoints, "CgPoint")
        # Fill of CgPoint attributes
        if "point_name" in kwargs:
            cgpoint.set("name", str(kwargs["point_name"]))
        if "pid" in kwargs:
            cgpoint.set("pntRef", str(kwargs["pid"]))
        if "x" in kwargs:
            cgpoint.text = "%s %s %s" % (str(kwargs["x"]),
                                         str(kwargs["y"]),
                                         str(kwargs["z"]))
        # attrib is not mandatory in CgPoints so this is a feature
        if "attrib" in kwargs:
            if cgpoints.find("./Feature") is None:
                feature = xml.SubElement(cgpoints, "Feature")
            feature = cgpoints.find("./Feature")
            # feature_property
            for i in range(len(kwargs["attrib"])):
                xml.SubElement(feature, "Property",
                               label="attrib%s" % (i + 1),
                               value=str(kwargs["attrib"][i]))

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

    def raw_observation(self, **kwargs):
        """
        Populate the RawObservation tag.

        No attribut is mandatory so kwargs can be empty.

        Arguments in kwargs for RawObservation:
            - th              -> targetHeight        attrib  of RawObservation
            - angle           -> horizAngle          attrib  of RawObservation
            - z_angle         -> zenithAngle         attrib  of RawObservation
            - slope_dist      -> slopeDistance       attrib  of RawObservation
            - horizontal_dist -> horizDistance       attrib  of RawObservation
            - point_name      -> desc                attrib  of TargetPoint part of RawObservation
            - pid             -> pntRef              attrib  of TargetPoint part of RawObservation
            - x               -> x coordinate        element of TargetPoint part of RawObservation
            - y               -> y coordinate        element of TargetPoint part of RawObservation
            - z               -> z coordinate        element of TargetPoint part of RawObservation
            - ih              -> instrumentHeight    attrib  of Property part of Feature
            - ppm             -> edmAccuracyppm      attrib  of Property part of Feature
            - prism_constant  -> edmAccuracyConstant attrib  of Property part of Feature
            - attrib          -> attribX             attrib  of Property part of Feature
        """

        # kwargs = {key: str(value) if value is not None else value for key,value in kwargs.items()}
        # When creating a RawObservation tag, it should verified that an ObservationGroup tag exists
        if self.survey.find("./ObservationGroup[@id='o0']") is None:
            self.setup()
        observation_group = self.survey.find("./ObservationGroup[@id='o%s']" % str(self.id - 1))
        # Creation of RawObservation tag, subelement of ObservationGroup
        raw_observation = xml.SubElement(observation_group, "RawObservation")
        # Fill of RawObservation attributes
        if "th" in kwargs:
            raw_observation.set("targetHeight", str(kwargs["th"]))
        if "angle" in kwargs:
            raw_observation.set("horizAngle", str(kwargs["angle"]))
        if "z_angle" in kwargs:
            raw_observation.set("zenithAngle", str(kwargs["z_angle"]))
        if "slope_dist" in kwargs and kwargs["slope_dist"] is not None:
            raw_observation.set("slopeDistance", str(kwargs["slope_dist"]))
        if "horizontal_dist" in kwargs and kwargs["horizontal_dist"] is not None:
            raw_observation.set("horizDistance", str(kwargs["horizontal_dist"]))
        # Creation of TargetPoint tag, subelement of RawObservation
        target_point = xml.SubElement(raw_observation, "TargetPoint")
        # Fill of TargetPoint attributes
        if "point_name" in kwargs:
            target_point.set("desc", str(kwargs["point_name"]))
        if "pid" in kwargs:
            target_point.set("pntRef", str(kwargs["pid"]))
        if "x" in kwargs:
            target_point.text = "%s %s %s" % (str(kwargs["x"]),
                                              str(kwargs["y"]),
                                              str(kwargs["z"]))
        # targetHeight is not mandatory in RawObservation so this is a feature
        if "ih" in kwargs and kwargs["ih"] is not None:
            if raw_observation.find("./Feature") is None:
                feature = xml.SubElement(raw_observation, "Feature")
            # feature_property
            xml.SubElement(feature, "Property",
                           label="instrumentHeight",
                           value=str(kwargs["ih"]))
        # ppm or prism_constant are not mandatory in RawObservation so this is a feature
        if "ppm" in kwargs and kwargs["ppm"] is not None:
            if raw_observation.find("./Feature") is None:
                feature = xml.SubElement(raw_observation, "Feature")
            # feature_property
            xml.SubElement(feature, "Property",
                           label="edmAccuracyppm",
                           value=str(kwargs["ppm"]))
            xml.SubElement(feature, "Property",
                           label="edmAccuracyConstant",
                           value=str(kwargs["prism_constant"]))
        # attrib is not mandatory in RawObservation so this is a feature
        if "attrib" in kwargs:
            if raw_observation.find("./Feature") is None:
                feature = xml.SubElement(raw_observation, "Feature")
            # feature_property
            for i in range(len(kwargs["attrib"])):
                xml.SubElement(feature, "Property",
                               label="attrib%s" % (i + 1),
                               value=str(kwargs["attrib"][i]))

    def to_string(self):
        """
        :return:
        """
        return xml.tostring(self.survey)


class LandXML:
    """
    Create the LandXML file.
    """

    def __init__(self):
        xml.register_namespace('', DEFAULT_NS)
        tree = xml.ElementTree(xml.fromstring(TEMPLATE))
        self.root = tree.getroot()

    def append(self, xml_data):
        self.root.append(xml_data)

    def to_string(self):
        self.root.set("date", time.strftime("%Y-%m-%d"))
        self.root.set("time", time.strftime("%H:%M:%S"))
        pretty_xml = _indent(self.root)
        return xml.tostring(pretty_xml)
