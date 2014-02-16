import unittest

from totalopenstation.formats.nikon_raw_v200 import FormatParser


class TestNikonParser(unittest.TestCase):

    def setUp(self):
        testdata = """
CO,Coord Order: NEZ
ST,1,,,,1.430,0.0000,0.0000
F1,,1.500,,0.0000,110.5344,13:47:08
SS,2,1.500,8.986,107.9916,102.3376,14:00:04,P
SS,3,1.500,7.706,110.4894,103.4372,14:00:51,P
SS,4,1.500,7.620,105.5898,104.3960,P"""
        self.fp = FormatParser(testdata)

    def test_points(self):
        self.assertAlmostEqual(self.fp.points[0][1], 8.9092817528619808)

    def test_shorter(self):
        self.assertEqual(self.fp.points[2][4], 'P')
