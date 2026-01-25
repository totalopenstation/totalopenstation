import unittest

import pytest

from totalopenstation.formats.geomax_txt import FormatParser

from . import BaseTestOutput


class TestGeomaxTXTParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/geomax/geomax_sample.txt') as testdata:
            self.fp = FormatParser(testdata.read())
            self.pts = list(self.fp.points)

    def test_points_count(self):
        """Test that all points are parsed."""
        self.assertEqual(len(self.pts), 5)

    def test_point_coordinates(self):
        """Test point coordinate parsing."""
        self.assertAlmostEqual(self.pts[0].geometry.x, 1000.0, places=3)
        self.assertAlmostEqual(self.pts[0].geometry.y, 2000.0, places=3)
        self.assertAlmostEqual(self.pts[0].geometry.z, 100.0, places=3)

    def test_point_attributes(self):
        """Test point attribute parsing."""
        self.assertEqual(self.pts[0].id, '1')
        self.assertEqual(self.pts[0].desc, 'POINT1')
        self.assertEqual(self.pts[2].desc, 'CORNER')

    def test_second_point(self):
        """Test second point parsing."""
        self.assertAlmostEqual(self.pts[1].geometry.x, 1001.5, places=3)
        self.assertAlmostEqual(self.pts[1].geometry.y, 2001.5, places=3)
        self.assertAlmostEqual(self.pts[1].geometry.z, 100.25, places=3)


class TestGeomaxTXTOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/geomax/geomax_sample.txt') as testdata:
            self.fp = FormatParser(testdata.read())
