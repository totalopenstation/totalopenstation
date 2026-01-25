import unittest

import pytest

from totalopenstation.formats.topcon_gpt import FormatParser

from . import BaseTestOutput


class TestTopconGPTParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/topcon/topcon_gpt_sample.txt') as testdata:
            self.fp = FormatParser(testdata.read())
            self.pts = list(self.fp.points)

    def test_points_count(self):
        """Test that all points are parsed."""
        self.assertEqual(len(self.pts), 5)

    def test_point_coordinates(self):
        """Test point coordinate parsing."""
        self.assertAlmostEqual(self.pts[0].geometry.x, 1000.0, places=2)
        self.assertAlmostEqual(self.pts[0].geometry.y, 2000.0, places=2)
        self.assertAlmostEqual(self.pts[0].geometry.z, 100.0, places=2)

    def test_point_id(self):
        """Test point ID parsing."""
        self.assertEqual(self.pts[0].id, '1')


class TestTopconGPTOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/topcon/topcon_gpt_sample.txt') as testdata:
            self.fp = FormatParser(testdata.read())
