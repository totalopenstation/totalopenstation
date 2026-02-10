# -*- coding: utf-8 -*-
# filename: tests/test_trimble_jxl.py
# Copyright 2025 Enzo Cocca <enzo.ccc@gmail.com>

import unittest

from totalopenstation.formats.trimble_jxl import FormatParser


SAMPLE_JXL = '''<?xml version="1.0" encoding="UTF-8"?>
<JOBFile jobName="TEST_JOB" version="5.72" product="Trimble General Survey" productVersion="3.21" TimeStamp="2025-04-22T15:02:35">
    <FieldBook>
        <UnitsRecord ID="00000002" TimeStamp="2025-04-22T15:02:35">
            <DistanceUnits>Metres</DistanceUnits>
            <AngleUnits>DMSDegrees</AngleUnits>
            <CoordinateOrder>North-East-Elevation</CoordinateOrder>
        </UnitsRecord>

        <InstrumentRecord ID="00000022" TimeStamp="2025-04-22T15:05:07">
            <Model>Trimble C5 3"</Model>
            <Serial>E091074</Serial>
        </InstrumentRecord>

        <PointRecord ID="00000027" TimeStamp="2025-04-22T15:05:30">
            <Name>100</Name>
            <Code>ST</Code>
            <Method>KeyedIn</Method>
            <Classification>Normal</Classification>
            <Deleted>false</Deleted>
            <Grid>
                <North>1000.000</North>
                <East>2000.000</East>
                <Elevation>100.000</Elevation>
            </Grid>
        </PointRecord>

        <PointRecord ID="00000028" TimeStamp="2025-04-22T15:06:00">
            <Name>101</Name>
            <Code>TOPO</Code>
            <Method>DirectReading</Method>
            <Classification>Normal</Classification>
            <Deleted>false</Deleted>
            <Circle>
                <HorizontalCircle>45.5</HorizontalCircle>
                <VerticalCircle>90.0</VerticalCircle>
                <EDMDistance>10.5</EDMDistance>
                <Face>Face1</Face>
            </Circle>
            <StationID>0000002b</StationID>
            <ComputedGrid>
                <North>1010.500</North>
                <East>2010.500</East>
                <Elevation>100.250</Elevation>
            </ComputedGrid>
        </PointRecord>

        <PointRecord ID="00000029" TimeStamp="2025-04-22T15:07:00">
            <Name>102</Name>
            <Code>REF</Code>
            <Method>DirectReading</Method>
            <Classification>BackSight</Classification>
            <Deleted>false</Deleted>
            <ComputedGrid>
                <North>1020.000</North>
                <East>2020.000</East>
                <Elevation>100.500</Elevation>
            </ComputedGrid>
        </PointRecord>

        <PointRecord ID="deleted" TimeStamp="2025-04-22T15:08:00">
            <Name>DELETED</Name>
            <Code>DEL</Code>
            <Deleted>true</Deleted>
            <Grid>
                <North>0</North>
                <East>0</East>
                <Elevation>0</Elevation>
            </Grid>
        </PointRecord>

        <StationRecord ID="0000002b" TimeStamp="2025-04-22T15:06:28">
            <StationName>100</StationName>
            <TheodoliteHeight>1.5</TheodoliteHeight>
            <StationType>StationSetupPlus</StationType>
        </StationRecord>

    </FieldBook>
</JOBFile>
'''


class TestTrimbleJXLParser(unittest.TestCase):

    def setUp(self):
        self.parser = FormatParser(SAMPLE_JXL)

    def test_point_count(self):
        """Test that parser extracts correct number of points."""
        points = self.parser.points
        # Should have 3 points (100, 101, 102) - DELETED is excluded
        self.assertEqual(len(points), 3)

    def test_point_names(self):
        """Test that point names are extracted correctly."""
        points = self.parser.points
        names = [p.id for p in points]
        self.assertIn('100', names)
        self.assertIn('101', names)
        self.assertIn('102', names)
        self.assertNotIn('DELETED', names)

    def test_point_coordinates_grid(self):
        """Test coordinates from Grid element (small values, no swap)."""
        points = self.parser.points
        point_100 = next(p for p in points if p.id == '100')
        # Small values: no swap applied, standard interpretation
        # East tag value -> x, North tag value -> y
        self.assertEqual(point_100.geometry.x, 2000.0)
        self.assertEqual(point_100.geometry.y, 1000.0)
        self.assertEqual(point_100.geometry.z, 100.0)

    def test_point_coordinates_computed_grid(self):
        """Test coordinates from ComputedGrid element (preferred)."""
        points = self.parser.points
        point_101 = next(p for p in points if p.id == '101')
        # Should use ComputedGrid values
        self.assertEqual(point_101.geometry.x, 2010.5)
        self.assertEqual(point_101.geometry.y, 1010.5)
        self.assertEqual(point_101.geometry.z, 100.25)

    def test_point_description(self):
        """Test point description/code."""
        points = self.parser.points
        point_100 = next(p for p in points if p.id == '100')
        self.assertEqual(point_100.desc, 'ST')

    def test_backsight_classification(self):
        """Test that BackSight classification is included in description."""
        points = self.parser.points
        point_102 = next(p for p in points if p.id == '102')
        self.assertIn('BackSight', point_102.desc)

    def test_polar_data_extraction(self):
        """Test that polar observation data is extracted."""
        points = self.parser.points
        point_101 = next(p for p in points if p.id == '101')
        self.assertEqual(point_101.properties.get('angle'), 45.5)
        self.assertEqual(point_101.properties.get('z_angle'), 90.0)
        self.assertEqual(point_101.properties.get('slope_dist'), 10.5)
        self.assertEqual(point_101.properties.get('face'), 'Face1')

    def test_deleted_points_excluded(self):
        """Test that deleted points are not included."""
        points = self.parser.points
        names = [p.id for p in points]
        self.assertNotIn('DELETED', names)

    def test_station_extraction(self):
        """Test station setup extraction."""
        stations = self.parser.get_stations()
        self.assertEqual(len(stations), 1)
        self.assertEqual(stations[0]['name'], '100')
        self.assertEqual(stations[0]['instrument_height'], 1.5)

    def test_job_info(self):
        """Test job metadata extraction."""
        info = self.parser.get_job_info()
        self.assertEqual(info['job_name'], 'TEST_JOB')
        self.assertEqual(info['product'], 'Trimble General Survey')
        self.assertEqual(info['instrument_model'], 'Trimble C5 3"')

    def test_invalid_xml(self):
        """Test handling of invalid XML."""
        parser = FormatParser("not valid xml")
        points = parser.points
        self.assertEqual(len(points), 0)

    def test_empty_xml(self):
        """Test handling of empty/minimal XML."""
        parser = FormatParser('<?xml version="1.0"?><JOBFile></JOBFile>')
        points = parser.points
        self.assertEqual(len(points), 0)

    def test_utm_coordinate_swap(self):
        """Test automatic coordinate swap for UTM values (Trimble convention).

        Trimble JXL files often store coordinates with North/East tags inverted
        when using UTM projection. The parser detects this by checking if
        North tag value < 1M and East tag value > 1M, then swaps them.
        """
        utm_jxl = '''<?xml version="1.0" encoding="UTF-8"?>
<JOBFile jobName="UTM_TEST" version="5.72">
    <FieldBook>
        <PointRecord ID="001">
            <Name>UTM_POINT</Name>
            <Code>TEST</Code>
            <Deleted>false</Deleted>
            <Grid>
                <North>374339.865</North>
                <East>4128109.803</East>
                <Elevation>64.623</Elevation>
            </Grid>
        </PointRecord>
    </FieldBook>
</JOBFile>'''
        parser = FormatParser(utm_jxl)
        points = parser.points
        self.assertEqual(len(points), 1)
        p = points[0]
        # North tag has small value (Easting), East tag has large value (Northing)
        # Parser should swap: x=374339 (Easting), y=4128109 (Northing)
        self.assertAlmostEqual(p.geometry.x, 374339.865, places=2)
        self.assertAlmostEqual(p.geometry.y, 4128109.803, places=2)


class TestTrimbleJXLWithSampleFile(unittest.TestCase):
    """Test with actual sample file."""

    def test_sample_file(self):
        """Test parsing the sample JXL file."""
        import os
        sample_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'sample_data', 'trimble', 'trimble_jxl_sample.jxl'
        )
        if os.path.exists(sample_path):
            with open(sample_path, 'r') as f:
                data = f.read()
            parser = FormatParser(data)
            points = parser.points
            # Sample file has 4 non-deleted points
            self.assertEqual(len(points), 4)


if __name__ == '__main__':
    unittest.main()
