import unittest

from totalopenstation.formats.zeiss_rec_500 import FormatParser

class TestZeissParser(unittest.TestCase):

    def setUp(self):
        testdata = '   0076                 576  A28    X       72.702 Y       -92.823 Z   156.620 '
        self.fp = FormatParser(testdata)

    def test_zeiss(self):
        assert self.fp.is_point(self.fp.data) == True
        assert self.fp.points[0][2] == '72.702'
        assert len(self.fp.points) == 1

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
