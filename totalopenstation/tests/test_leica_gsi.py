import unittest

from totalopenstation.formats.leica_gsi import FormatParser


class TestLeicaGSI16Parser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/leica_gsi/leica_gsi16_gurob.gsi') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, 8.0757244)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 11.21674196)
        self.assertAlmostEqual(self.fp.points[0].geometry.z, -0.2890493)

    def test_feature(self):
        self.assertEqual(self.fp.points[0].id, '0002')
        self.assertEqual(self.fp.points[0].desc, 'GDEM5415')
        self.assertEqual(self.fp.points[1].desc, 'GDEM5416')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[0][0], 8.0757244)


class TestLeicaGSI8Parser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/leica_gsi/leica_gsi8_ertola.gsi') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, 515.836)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 525.871)
        self.assertAlmostEqual(self.fp.points[0].geometry.z, 3.079)

    def test_feature(self):
        self.assertEqual(self.fp.points[0].id, '0001')
        self.assertEqual(self.fp.points[0].desc, '1')
        self.assertEqual(self.fp.points[1].desc, '2')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[0][0], 515.836)
        self.assertAlmostEqual(self.ls.coords[3][2], 2.553)
        self.assertAlmostEqual(self.ls.bounds[0], 0.0)
