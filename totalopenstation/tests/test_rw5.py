import unittest

from totalopenstation.formats.carlson_rw5 import FormatParser

class TestCarlsonRW5Parser(unittest.TestCase):
    def setUp(self):
        with open('sample_data/Leica1200.rw5') as testdata:
            fp = FormatParser(testdata.read())
            self.pts = list(fp.points)

    def test_point(self):
        self.assertEqual(self.pts[0][0], '108')
        self.assertAlmostEqual(self.pts[0][2], 942130.662, places=3)
        self.assertAlmostEqual(self.pts[0][1], 16556174.237, places=3)
        self.assertAlmostEqual(self.pts[0][3], 20.053, places=3)
        self.assertEqual(self.pts[0][4], 'FENCE1')
        self.assertEqual(self.pts[1][4], 'LIGHT POLE')

