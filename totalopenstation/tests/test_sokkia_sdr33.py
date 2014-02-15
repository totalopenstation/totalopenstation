import unittest

from totalopenstation.formats.sokkia_sdr33 import FormatParser


class TestSokkiaParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/sokkia_sdr33.tops') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertEqual(self.fp.points[0][0], 31)
        self.assertAlmostEqual(self.fp.points[0][2], 509.970)
        self.assertAlmostEqual(self.fp.points[0][1], 937.274)
        self.assertAlmostEqual(self.fp.points[0][3], 20.053)
        self.assertEqual(self.fp.points[0][4], '11')
        self.assertEqual(self.fp.points[1][4], '11')

