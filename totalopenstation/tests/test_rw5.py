import unittest

import pytest

from totalopenstation.formats.carlson_rw5 import FormatParser

from . import BaseTestOutput


class TestCarlsonRW5Parser(unittest.TestCase):
    def setUp(self):
        with open('sample_data/carlson_rw5/Leica1200.rw5') as testdata:
            fp = FormatParser(testdata.read())
            self.pts = list(fp.points)

    def test_point_xy(self):
        self.assertAlmostEqual(self.pts[0].geometry.x, 942130.662, places=3)
        self.assertAlmostEqual(self.pts[0].geometry.y, 16556174.237, places=3)

    @unittest.expectedFailure
    def test_point_z(self):
        self.assertAlmostEqual(self.pts[0].geometry.z, 20.053, places=3)

    def test_feature(self):
        self.assertEqual(self.pts[1].point_name, '108')
        self.assertEqual(self.pts[2].id, 2)
        self.assertEqual(self.pts[4].properties['attrib'][0], 'LIGHT POLE')
        self.assertEqual(self.pts[3].desc, 'PT')



class TestRW5Output(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/carlson_rw5/Leica1200.rw5') as testdata:
            self.fp = FormatParser(testdata.read())
