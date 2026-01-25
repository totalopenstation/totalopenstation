import unittest

from totalopenstation.formats import Feature, LineString, Point
from totalopenstation.output.tops_dxf import OutputFormat


class TestDXFOutput(unittest.TestCase):

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

    def test_output_is_valid_dxf(self):
        """Test that output is a valid DXF string."""
        output = OutputFormat(self.data, separate_layers=False).process()
        # Check DXF structure markers
        self.assertIn('SECTION', output)
        self.assertIn('ENDSEC', output)
        self.assertIn('EOF', output)

    def test_output_contains_layers(self):
        """Test that layers are created correctly."""
        output = OutputFormat(self.data, separate_layers=False).process()
        self.assertIn('TESTPOINT', output)
        self.assertIn('TESTPOINT2', output)
        self.assertIn('TESTLINE', output)

    def test_output_separate_layers(self):
        """Test that separate layers are created when enabled."""
        output = OutputFormat(self.data, separate_layers=True).process()
        self.assertIn('TESTPOINT_POINTS', output)
        self.assertIn('TESTPOINT_LABELS', output)
        self.assertIn('TESTPOINT_Z_COORDS', output)

    def test_output_contains_points(self):
        """Test that point entities are in the output."""
        output = OutputFormat(self.data, separate_layers=False).process()
        self.assertIn('POINT', output)

    def test_output_contains_text(self):
        """Test that text entities are in the output."""
        output = OutputFormat(self.data, separate_layers=False).process()
        self.assertIn('TEXT', output)

    def test_output_contains_polyline(self):
        """Test that polyline entities are in the output."""
        output = OutputFormat(self.data, separate_layers=False).process()
        self.assertIn('POLYLINE', output)

    def test_output_contains_coordinates(self):
        """Test that coordinates are in the output."""
        output = OutputFormat(self.data, separate_layers=False).process()
        # Check for coordinate values (as strings in DXF)
        self.assertIn('12.8', output)
        self.assertIn('76.3', output)
        self.assertIn('56.2', output)

    def test_can_be_parsed_by_ezdxf(self):
        """Test that output can be parsed back by ezdxf."""
        import io
        import ezdxf

        output = OutputFormat(self.data, separate_layers=False).process()
        stream = io.StringIO(output)
        doc = ezdxf.read(stream)

        # Check that we have the expected entities
        msp = doc.modelspace()
        entities = list(msp)

        # Should have: 2 points + 2 ID texts + 2 Z texts + 1 polyline = 7 entities
        self.assertGreaterEqual(len(entities), 7)
