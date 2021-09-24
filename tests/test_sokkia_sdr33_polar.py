import unittest

import pytest

from totalopenstation.formats.sokkia_sdr33 import FormatParser

from __init__ import BaseTestOutput


class TestSokkiaParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/sokkia_sdr33_polar.tops') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.coords[0][1], 0.000)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 0.000)
        self.assertAlmostEqual(self.fp.points[0].geometry.coords[0][0], 0.000)
        self.assertAlmostEqual(self.fp.points[0].geometry.coords[0][2], 0.000)

    def test_feature(self, STZTEMP=None):
        self.assertEqual(self.fp.points[0].id, STZTEMP)
        self.assertEqual(self.fp.points[0].desc, 'STZTEMP')
        self.assertEqual(self.fp.points[1].desc, 'STZTEMP')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[0][0], 0.0)


class TestSokkiaOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/sokkia_sdr33_polar.tops') as testdata:
            self.fp = FormatParser(testdata.read())
