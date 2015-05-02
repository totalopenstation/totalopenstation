import unittest

from totalopenstation.formats.leica_tcr_705 import FormatParser


class TestLeicaTCR705Parser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/leica_tcr_705') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[1].geometry.x, 1002.825)
        self.assertAlmostEqual(self.fp.points[1].geometry.y, 999.529)
        self.assertAlmostEqual(self.fp.points[1].geometry.z, 98.430)

    def test_feature(self):
        self.assertEqual(self.fp.points[1].id, '101')
        self.assertEqual(self.fp.points[1].desc, 'WALL01')
        self.assertEqual(self.fp.points[0].desc, 'WALL01')
