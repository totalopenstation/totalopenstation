import unittest

import pytest

from totalopenstation.formats.nikon_raw_v200 import FormatParser

from . import BaseTestOutput


class TestNikonParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/nikon_raw_v200/nikon_raw_v200.tops') as testdata:
            self.fp = FormatParser(testdata.read())
        with open('sample_data/nikon_raw_v200/nikon_dtm.tops') as testdata2:
            self.fp2 = FormatParser(testdata2.read())

    def test_points(self):
        self.assertAlmostEqual(self.fp.points[1].geometry.x, 0.0)

    def test_basepoint(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, 0.0)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 0.0)
        self.assertAlmostEqual(self.fp2.points[7].geometry.x, 10000.08905808)
        self.assertAlmostEqual(self.fp2.points[7].geometry.y, 10000.30257267)

    def test_feature(self):
        self.assertEqual(self.fp.points[3].id, 3)
        self.assertEqual(self.fp.points[3].desc, 'PT')


class TestNikonRAWOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/nikon_raw_v200/nikon_raw_v200.tops') as testdata:
            self.fp = FormatParser(testdata.read())


class TestNikonRAW2Output(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/nikon_raw_v200/nikon_dtm.tops') as testdata:
            self.fp = FormatParser(testdata.read())
