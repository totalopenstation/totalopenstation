import unittest

from totalopenstation.formats.nikon_raw_v200 import FormatParser


class TestNikonParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/nikon_raw_v200.tops') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_points(self):
        self.assertAlmostEqual(self.fp.points[0][1], 8.9092817528619808)

    def test_shorter(self):
        self.assertEqual(self.fp.points[2][4], 'P')

    def test_correction(self):
        self.assertAlmostEqual(self.fp.points[54][2], -3.787)
        self.assertAlmostEqual(self.fp.points[54][1], 5.548)
        self.assertAlmostEqual(self.fp.points[54][3], -0.543)
