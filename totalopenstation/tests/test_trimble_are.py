import unittest

import pytest

from totalopenstation.formats.trimble_are import FormatParser

from . import BaseTestOutput


class TestTrimbleAREParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/trimble/BSG-08-11-19.are') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[1].geometry.x, 499.622)
        self.assertAlmostEqual(self.fp.points[1].geometry.y, 497.857)
        self.assertAlmostEqual(self.fp.points[1].geometry.z, 1.348)

    def test_feature(self):
        self.assertEqual(self.fp.points[1].id, '3')
        self.assertEqual(self.fp.points[1].desc, 'FIX')
        self.assertEqual(self.fp.points[0].desc, 'TEST')


class TestTrimbleAREOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/trimble/BSG-08-11-19.are') as testdata:
            self.fp = FormatParser(testdata.read())
