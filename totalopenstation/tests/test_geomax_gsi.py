import unittest

import pytest

from totalopenstation.formats.geomax_gsi import FormatParser

from . import BaseTestOutput


class TestGeomaxGSIParser(unittest.TestCase):
    """Test Geomax GSI parser using Leica GSI sample data.

    Geomax GSI format is compatible with Leica GSI format.
    """

    def setUp(self):
        # Use existing Leica GSI sample data since formats are compatible
        with open('sample_data/leica_gsi/leica_gsi8_ertola.gsi') as testdata:
            self.fp = FormatParser(testdata.read())
            self.pts = list(self.fp.points)

    def test_points_count(self):
        """Test that points are parsed."""
        self.assertGreater(len(self.pts), 0)

    def test_point_has_geometry(self):
        """Test that parsed points have geometry."""
        self.assertIsNotNone(self.pts[0].geometry)
        self.assertIsNotNone(self.pts[0].geometry.x)
        self.assertIsNotNone(self.pts[0].geometry.y)


class TestGeomaxGSIOutput(BaseTestOutput):

    @pytest.fixture
    def setup(self):
        with open('sample_data/leica_gsi/leica_gsi8_ertola.gsi') as testdata:
            self.fp = FormatParser(testdata.read())
