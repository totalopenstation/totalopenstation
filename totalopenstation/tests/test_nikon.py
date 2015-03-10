import unittest

from totalopenstation.formats.nikon_raw_v200 import FormatParser


class TestNikonParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/nikon_raw_v200/nikon_raw_v200.tops') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_points(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, 8.9092817528619808)

    def test_feature(self):
        self.assertEqual(self.fp.points[2].id, '4')
        self.assertEqual(self.fp.points[2].desc, 'P')
