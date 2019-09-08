import unittest

import pytest

from totalopenstation.formats.zeiss_r5 import FormatParser

from . import BaseTestOutput


class TestZeissR5(unittest.TestCase):
    def setUp(self):
        with open('sample_data/zeiss_elta_r55/zeiss_elta_r55-R5.tops') as testdata:
            self.fp = FormatParser(testdata.read())
            self.feature = self.fp.points[11]
            self.point = self.feature.geometry

    def test_point(self):
        self.assertAlmostEqual(self.point.x, 6.554)
        self.assertAlmostEqual(self.point.y, 50.896)
        self.assertAlmostEqual(self.point.z, 11.334)

    def test_feature(self):
        self.assertEqual(self.feature.id, '1108')
        self.assertEqual(self.feature.desc, '67R')


class TestZeissR5Output(BaseTestOutput):
    @pytest.fixture
    def setup(self):
        with open('sample_data/zeiss_elta_r55/zeiss_elta_r55-R5.tops') as testdata:
            self.fp = FormatParser(testdata.read())
