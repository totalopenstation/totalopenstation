import unittest

import pytest

from totalopenstation.formats.leica_tcr_1205 import FormatParser

from . import BaseTestOutput


class TestLeicaTCR1205Parser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/leica_tcr_1205') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[1].geometry.x, 450402.042)
        self.assertAlmostEqual(self.fp.points[1].geometry.y, 205885.618)
        self.assertAlmostEqual(self.fp.points[1].geometry.z, 61.309)

    def test_feature(self):
        self.assertEqual(self.fp.points[1].id, '10001')
        self.assertEqual(self.fp.points[1].desc, 'Line0001')
        self.assertEqual(self.fp.points[2].desc, 'Line0001')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[6][0], 450403.738)
        self.assertAlmostEqual(self.ls.coords[6][1], 205883.360)
        self.assertAlmostEqual(self.ls.coords[6][2], 61.318)


class TestLeicaTCR1205Output(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/leica_tcr_1205') as testdata:
            self.fp = FormatParser(testdata.read())
