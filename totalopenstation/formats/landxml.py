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

from totalopenstation.formats.conversion import vertical_to_zenithal

import xml.etree.ElementTree as xml
import time
import re
import os

from . import Feature, Parser, Point, UNKNOWN_STATION, UNKNOWN_POINT
from .polar import BasePoint, PolarPoint

# Template string
TEMPLATE = '''<?xml version="1.0"?>
                <LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.landxml.org/schema/LandXML-1.2 http://www.landxml.org/schema/LandXML-1.2/LandXML-1.2.xsd" date="" time="" version="1.2">
                    <Units>
                        <Metric areaUnit="squareMeter" linearUnit="meter" volumeUnit="cubicMeter" temperatureUnit="celsius" pressureUnit="milliBars" angularUnit="grads" directionUnit="grads"></Metric>
                    </Units>
                    <Project name="Template"></Project>
                    <Application name="TotalOpen Station" desc="TOPS" manufacturer="" version="" manufacturerURL="http://tops.iosa.it/" timeStamp=""></Application>
                </LandXML>'''

DEFAULT_NS = "http://www.landxml.org/schema/LandXML-1.2"
DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'


def _indent(elem, level=0):
    """
    A function to indent a XML Element for pretty printing
    :param elem: The element to parse
    :param level: The level of the element in the hierarchy
    :return: The element ready to be pretty printed

    Note : Taken from https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python/4590052#4590052
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
        """
        Search the position of the tag to be in the right order
        """
        mainTags = ("SurveyHeader", "Equipment", "CgPoints", "InstrumentSetup")
        if tag in mainTags:
            pos = 0
    
            for index in range(mainTags.index(tag)):
                if self.survey.find("./%s" % mainTags[index]) is not None:
                    pos += 1
                else:
                    pos = 1
    
            if tag == "InstrumentSetup":
                pos += len(self.survey.findall("./InstrumentSetup"))
    
            return pos
        if tag == "CgPoint":
            cgpoints = self.survey.find("CgPoints")
            pos = len(cgpoints.findall("./CgPoint"))
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
        
        All Feature tags should be after Cgpoint ones
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
        cgpoint = xml.Element("CgPoint")
        cgpoints.insert(self._tag_position('CgPoint'), cgpoint)
        # Fill of CgPoint attributes
        if "point_name" in kwargs:
            cgpoint.set("name", str(kwargs["point_name"]))
        if "pid" in kwargs:
            cgpoint.set("pntRef", str(kwargs["pid"]))
        if "x" in kwargs:
            cgpoint.text = "%s %s" % (str(kwargs["x"]),
                                         str(kwargs["y"]))
            if "z" in kwargs:
                cgpoint.text += " %s" % (str(kwargs["z"]))
        # attrib is not mandatory in CgPoints so this is a feature
        if "attrib" in kwargs:
            cgpoint.set("featureRef", "feature%s" % (str(kwargs["point_name"])))
            feature = xml.Element("Feature")
            feature.set("name", "feature%s" % (str(kwargs["point_name"])))
            # feature_property
            for i in range(len(kwargs["attrib"])):
                xml.SubElement(feature, "Property",
                              label="attrib%s" % (i + 1),
                              value=str(kwargs["attrib"][i]))
            cgpoints.append(feature)

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
                                        id="o" + str(self.id),
                                        setupID="setup" + str(self.id))
        # Creation of Backsight tag, subelement of ObservationGroup
        if "circle" in kwargs or "back_x" in kwargs:
            backsight = xml.SubElement(observation_group, "Backsight",
                                       circle="0.")
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
            - dist            -> Distance            attrib  of RawObservation
            - dist_type       -> Type of distance    attrib  of RawObservation
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
        if "angle" in kwargs and kwargs["angle"] is not None:
            raw_observation.set("horizAngle", str(kwargs["angle"]))
        if "azimuth" in kwargs and kwargs["azimuth"] is not None:
            raw_observation.set("azimuth", str(kwargs["azimuth"]))
        if "z_angle" in kwargs and kwargs["z_angle"] is not None:
            if kwargs["z_angle_type"] == "dh":
                raw_observation.set("vertDistance", str(kwargs["z_angle"]))
            if kwargs["z_angle_type"] == "z":
                raw_observation.set("zenithAngle", str(kwargs["z_angle"]))
            if kwargs["z_angle_type"] == "v":
                raw_observation.set("zenithAngle", str(vertical_to_zenithal(kwargs["z_angle"],kwargs["angle_unit"])))
        if "dist" in kwargs and kwargs["dist"] is not None:
            if kwargs["dist_type"] == 's':
                raw_observation.set("slopeDistance", str(kwargs["dist"]))
            if kwargs["dist_type"] == 'h':
                raw_observation.set("horizDistance", str(kwargs["dist"]))
        # Creation of TargetPoint tag, subelement of RawObservation
        target_point = xml.SubElement(raw_observation, "TargetPoint")
        # Fill of TargetPoint attributes
        if "point_name" in kwargs:
            target_point.set("desc", str(kwargs["point_name"]))
        if "pid" in kwargs:
            target_point.set("pntRef", str(kwargs["pid"]))
        if "x" in kwargs:
            target_point.text = "%s %s" % (str(kwargs["x"]),
                                           str(kwargs["y"]))
            if "z" in kwargs:
                target_point.text += " %s" % (str(kwargs["z"]))
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
        cdate = time.strftime("%Y-%m-%d")
        ctime = time.strftime("%H:%M:%S")
        self.root.set("date", cdate)
        self.root.set("time", ctime)
        application = self.root.find("{%s}Application" % (DEFAULT_NS))
        application.set("timeStamp", "%sT%s" % (cdate, ctime))
        pretty_xml = _indent(self.root)
        return xml.tostring(pretty_xml).decode()


class FormatParser(Parser):
    """
    A FormatParser for LandXML data format.

    As the model data is in LandXML format, only Survey tags is kept.

    It doesn't inherit from the base Parser class because the internal
    procedure is quite different, but it implements the same API so it
    can work nicely with other parts of the library.
    """

    def __init__(self, data):
        data = re.sub('(\\n|\\t)', '', data)
        self.line = xml.fromstring(data) 

    @property
    def points(self):
        '''Compute raw data to get points coordinates.

        This parser is based on the information in :ref:`if_landxml`
        
        Returns:
            A list of GeoJSON-like Feature object representing points coordinates.
    
        Raises:
            KeyError: An error occured during computation, the data does not exist.
        
        Notes:
        '''
        points = []
        stations = {}
        pointsFeature = self.raw_line

        for point in pointsFeature:
            if point.desc == 'PT':
                points.append(point)
            if point.desc == 'ST':
                stations[point.point_name] = point
            if point.desc == 'PO':
                pp = point.properties
                coords = stations[pp['station_name']].geometry
                bp = BasePoint(x=coords.x, y=coords.y, z=coords.z, ih=pp['ih'], b_zero_st=0.0)
                p = PolarPoint(angle_unit=pp['angle_unit'],
                                z_angle_type=pp['z_angle_type'],
                                dist_type=pp['dist_type'],
                                dist=pp['dist'],
                                angle=pp['angle'],
                                z_angle=pp['z_angle'],
                                th=pp['th'],
                                base_point=bp,
                                pid=point.id,
                                text='',
                                coordorder='ENZ')
                f = Feature(p.to_point(),
                            desc='PT',
                            id=point.id,
                            point_name=point.point_name)
                points.append(f)

        return points

    @property
    def raw_line(self):
        '''Extract all LandXML data.

        This parser is based on the information in :ref:`if_landxml`

        Returns:
            A list of GeoJSON-like Feature object representing raw data
            i.e. polar coordinates and other informations.

        Raises:

        Notes:
        '''

        ns = {"default": DEFAULT_NS}
        stations = {}
        points = []
        points_coord = {}
        pid = 0
        station_id = 1

        # These values are mandatory by the LandXML schema
        units = self.line.find("default:Units", ns)
        dist_unit = units.find("default:Metric", ns).attrib["linearUnit"]
        angle_unit = units.find("default:Metric", ns).attrib["angularUnit"]

        survey = self.line.find("default:Survey", ns)
        cgpoints = survey.find("default:CgPoints", ns)
        point_id = 100
        for cgpoint in cgpoints.findall("default:CgPoint", ns):
            p = Point(cgpoint.text.split(" "))
            try:
                point_name = cgpoint.attrib["name"]
            except KeyError:
                point_name = "point_" + str(point_id)
                point_id += 1
            points_coord[point_name] = p
            feature = cgpoints.find(f"""default:Feature[@name='{cgpoint.attrib["featureRef"]}']""", ns)
            if feature is not None:
               attrib = [prop.attrib["value"] for prop in feature.findall("default:Property", ns)]
            f = Feature(p,
                        desc='PT',
                        id=pid,
                        point_name=point_name,
                        dist_unit=dist_unit,
                        attrib=attrib)
            points.append(f)
            pid += 1
        for station in survey.findall("default:InstrumentSetup", ns):
            station_id = station.attrib["id"]
            point_name = station.attrib["stationName"]
            p = points_coord[point_name] 
            ih = station.attrib["instrumentHeight"]
            stations[station_id] = [point_name, ih]
            try :
                hz0 = station.attrib["orientationAzimuth"]
            except KeyError:
                try :
                    hz0 = station.attrib["circleAzimuth"]
                except KeyError:
                    hz0 = None
            feature = station.find("default:Feature", ns)
            if feature is not None:
                attrib = [prop.attrib["value"] for prop in feature.findall("default:Property", ns)]
            f = Feature(p,
                        desc='ST',
                        id=pid,
                        point_name=point_name,
                        angle_unit=angle_unit,
                        dist_unit=dist_unit,
                        ih=ih,
                        hz0=hz0,
                        attrib=attrib)
            points.append(f)
            pid += 1
        point_id = 100
        for observation in survey.findall("default:ObservationGroup", ns):
            try:
                station_id = observation.attrib["setupID"]
            except:
                station_id = ''
            for rawobservation in observation.findall("default:RawObservation", ns):
                if not station_id:
                    try:
                        station_id = rawobservation.attrib["setupID"]
                    except:
                        pass
                target_point = rawobservation.find("default:TargetPoint", ns)
                if target_point is not None:
                    try:
                        point_name = target_point.attrib["desc"]
                    except KeyError:
                        try:
                            point_name = target_point.attrib["name"]
                        except KeyError:
                            point_name = "point_" + point_id
                            point_id += 1
                    p = Point(target_point.text.split(" "))
                try:
                    azimuth = rawobservation.attrib["azimuth"]
                except KeyError:
                    azimuth = None
                try:
                    angle = rawobservation.attrib["horizAngle"]
                except KeyError:
                    angle = None
                try:
                    z_angle = rawobservation.attrib["zenithAngle"]
                    z_angle_type = 'z'
                except KeyError:
                    z_angle = None
                # dZ
                #     z_angle = rawobservation.attrib["vertDistance"]
                #     z_angle_type = 'dh'
                try:
                    dist = rawobservation.attrib["slopeDistance"]
                    dist_type = 's'
                except KeyError:
                    try:
                        dist =  rawobservation.attrib["horizDistance"]
                        dist_type = 'h'
                    except KeyError:
                        dist = None
                try:
                    th = rawobservation.attrib["targetHeight"]
                except KeyError:
                    th = None
                # ih is integrated in point values to simplify possible computation
                ih = stations[station_id][1]
                station_name = stations[station_id][0]
                
                feature = rawobservation.find("default:Feature", ns)
                if feature is not None:
                    attrib = [prop.attrib["value"] for prop in feature.findall("default:Property", ns)]
                f = Feature(p,
                            desc='PO',
                            id=pid,
                            point_name=point_name,
                            angle_unit=angle_unit,
                            z_angle_type=z_angle_type,
                            dist_unit=dist_unit,
                            dist_type=dist_type,
                            azimuth=azimuth,
                            angle=angle,
                            z_angle=z_angle,
                            dist=dist,
                            ih=ih,
                            th=th,
                            station_name=station_name,
                            attrib=attrib)
                points.append(f)
                pid += 1

        return points