import unittest

import pytest

from totalopenstation.formats.sokkia_sdr33 import FormatParser

from . import BaseTestOutput


class TestSokkiaParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/sokkia_sdr33.tops') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.coords[0][1], 509.970)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 509.970)
        self.assertAlmostEqual(self.fp.points[0].geometry.coords[0][0], 937.274)
        self.assertAlmostEqual(self.fp.points[0].geometry.coords[0][2], 20.053)

    def test_feature(self):
        self.assertEqual(self.fp.points[0].id, 31)
        self.assertEqual(self.fp.points[0].desc, '11')
        self.assertEqual(self.fp.points[1].desc, '11')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[0][0], 937.274)


class TestSokkiaOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/sokkia_sdr33.tops') as testdata:
            self.fp = FormatParser(testdata.read())
