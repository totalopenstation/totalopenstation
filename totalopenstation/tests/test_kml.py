import unittest

from totalopenstation.formats import Feature, LineString, Point
from totalopenstation.output.tops_kml import OutputFormat


class TestKMLOutput(unittest.TestCase):

    def setUp(self):
        self.data = [
            Feature(Point(12.8, 76.3, 56.2),
                    desc='TESTPOINT',
                    id=1),
            Feature(Point(19.8, 26.3, 46.2),
                    desc='TESTPOINT2',
                    id=2),
            Feature(LineString(((17.8, 26.0, 41.2),
                                (18.8, 26.6, 44.2),
                                (24.8, 26.9, 42.2))),
                    desc='TESTLINE',
                    id=3),
        ]

    def test_output_is_valid_kml(self):
        """Test that output is a valid KML string."""
        output = OutputFormat(self.data).process()
        # Check KML structure
        self.assertIn('<?xml', output)
        self.assertIn('<kml', output)
        self.assertIn('</kml>', output)
        self.assertIn('<Document', output)

    def test_output_contains_folders(self):
        """Test that folders are created for each description."""
        output = OutputFormat(self.data).process()
        self.assertIn('<Folder', output)
        self.assertIn('TESTPOINT', output)
        self.assertIn('TESTPOINT2', output)
        self.assertIn('TESTLINE', output)

    def test_output_contains_points(self):
        """Test that point placemarks are in the output."""
        output = OutputFormat(self.data).process()
        self.assertIn('<Point id=', output)
        self.assertIn('<coordinates>', output)

    def test_output_contains_linestring(self):
        """Test that linestring is in the output."""
        output = OutputFormat(self.data).process()
        self.assertIn('<LineString id=', output)

    def test_output_contains_coordinates(self):
        """Test that coordinates are in the output."""
        output = OutputFormat(self.data).process()
        # Check for coordinate values
        self.assertIn('12.8', output)
        self.assertIn('76.3', output)
        self.assertIn('56.2', output)

    def test_output_contains_point_names(self):
        """Test that point IDs are used as names."""
        output = OutputFormat(self.data).process()
        self.assertIn('<name>1</name>', output)
        self.assertIn('<name>2</name>', output)
        self.assertIn('<name>3</name>', output)
