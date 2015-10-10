import unittest

from totalopenstation.formats.nikon_raw_v200 import FormatParser


class TestNikonParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/nikon_raw_v200/nikon_raw_v200.tops') as testdata:
            self.fp = FormatParser(testdata.read())
        with open('sample_data/nikon_raw_v200/nikon_dtm.tops') as testdata2:
            self.fp2 = FormatParser(testdata2.read())

    def test_points(self):
        self.assertAlmostEqual(self.fp.points[1].geometry.x, 8.9092817528619808)

    def test_basepoint(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, 0.0)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 0.0)
        self.assertAlmostEqual(self.fp2.points[7].geometry.x, 322.5024)
        self.assertAlmostEqual(self.fp2.points[7].geometry.y, 322.5024)

    def test_feature(self):
        self.assertEqual(self.fp.points[3].id, '4')
        self.assertEqual(self.fp.points[3].desc, 'P')
