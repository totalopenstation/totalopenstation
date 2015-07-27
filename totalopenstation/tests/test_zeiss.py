import unittest

from totalopenstation.formats.zeiss_rec_500 import FormatParser

class TestZeissParser(unittest.TestCase):

    def setUp(self):
        testdata = '   0076                 576  A28    X       72.702 Y       -92.823 Z   156.620 '
        self.fp = FormatParser(testdata)

    def test_zeiss(self):
        self.assertTrue(self.fp.is_point(self.fp.data))
        self.assertEqual(self.fp.points[0].geometry.y, 72.702)
        self.assertEqual(self.fp.points[0].geometry.x, -92.823)
        self.assertEqual(len(self.fp.points), 1)

class TestZeissExceptionValue(unittest.TestCase):

    def setUp(self):
        testdata = '   0076             576  A28    X       72.702 Y       -92.823 Z   156.620 '
        self.fp = FormatParser(testdata)

    def test_exceptions(self):
        self.assertRaises(ValueError, self.fp.get_point, self.fp.data)


class TestZeissExceptionIndex(unittest.TestCase):

    def setUp(self):
        testdata = 'END'
        self.fp = FormatParser(testdata)

    def test_exceptions(self):
        self.assertRaises(ValueError, self.fp.get_point, self.fp.data)
