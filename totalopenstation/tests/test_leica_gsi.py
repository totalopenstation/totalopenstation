import unittest

from totalopenstation.formats.leica_gsi import FormatParser


class TestLeicaGSI16Parser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/leica_gsi/leica_gsi16_gurob.gsi') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, 8.0169035)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 11.2596402)
        self.assertAlmostEqual(self.fp.points[0].geometry.z, -0.25952208)

    def test_feature(self):
        self.assertEqual(self.fp.points[0].id, '0002')
        self.assertEqual(self.fp.points[0].properties['desc'], 'GDEM5415')
        self.assertEqual(self.fp.points[1].properties['desc'], 'GDEM5416')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[0][0], 8.0169035)
