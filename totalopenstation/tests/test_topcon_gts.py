import unittest

import pytest

from totalopenstation.formats.topcon_gts import FormatParser

from . import BaseTestOutput

class TestTopconGTSParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/topcon_gts_229') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[0].geometry.x, -5247.0753003)
        self.assertAlmostEqual(self.fp.points[0].geometry.y, 5049.9025715)
        self.assertAlmostEqual(self.fp.points[0].geometry.z, 64289.3662938)

    def test_feature(self):
        self.assertEqual(self.fp.points[0].id, '2')
        self.assertEqual(self.fp.points[0].desc, '00099')
        self.assertEqual(self.fp.points[1].desc, '00101')

class TestTopconGTSOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/topcon_gts_229') as testdata:
            self.fp = FormatParser(testdata.read())
