import unittest

from totalopenstation.formats import Feature, Point
from totalopenstation.output import OutputOption, Builder
from totalopenstation.output.tops_csv import OutputFormat as CSVOutputFormat


class TestOutputOption(unittest.TestCase):

    def test_bool_option(self):
        """Test boolean option validation."""
        opt = OutputOption('test', 'Test Option', option_type='bool', default=True)
        self.assertTrue(opt.validate(True))
        self.assertFalse(opt.validate(False))
        self.assertTrue(opt.validate(1))
        self.assertFalse(opt.validate(0))

    def test_choice_option(self):
        """Test choice option validation."""
        opt = OutputOption('sep', 'Separator', option_type='choice',
                          default=',', choices=[',', ';', '\t'])
        self.assertEqual(opt.validate(','), ',')
        self.assertEqual(opt.validate(';'), ';')

        with self.assertRaises(ValueError):
            opt.validate('invalid')

    def test_number_option(self):
        """Test number option validation."""
        opt = OutputOption('scale', 'Scale', option_type='number', default=1.0)
        self.assertEqual(opt.validate(2.5), 2.5)
        self.assertEqual(opt.validate('3.14'), 3.14)

    def test_text_option(self):
        """Test text option validation."""
        opt = OutputOption('name', 'Name', option_type='text', default='')
        self.assertEqual(opt.validate('test'), 'test')
        self.assertEqual(opt.validate(123), '123')


class TestCSVOptions(unittest.TestCase):

    def setUp(self):
        self.data = [
            Feature(Point(12.8, 76.3, 56.2), desc='TESTPOINT', id=1),
            Feature(Point(19.8, 26.3, 46.2), desc='TESTPOINT2', id=2),
        ]

    def test_default_options(self):
        """Test CSV output with default options."""
        output = CSVOutputFormat(self.data).process()
        # Default separator is comma
        self.assertIn(',', output)
        # Default includes header
        self.assertIn('pid', output)
        # Default includes z
        self.assertIn('56.2', output)

    def test_custom_separator(self):
        """Test CSV output with custom separator."""
        output = CSVOutputFormat(self.data, separator=';').process()
        self.assertIn(';', output)

    def test_no_header(self):
        """Test CSV output without header."""
        output = CSVOutputFormat(self.data, include_header=False).process()
        self.assertNotIn('"pid"', output)
        # But data should still be there
        self.assertIn('12.8', output)

    def test_no_z_coordinates(self):
        """Test CSV output without Z coordinates."""
        output = CSVOutputFormat(self.data, include_z=False).process()
        # Z values should not be in output
        self.assertNotIn('56.2', output)
        # But X, Y should be there
        self.assertIn('12.8', output)
        self.assertIn('76.3', output)

    def test_get_options(self):
        """Test getting available options from format."""
        options = CSVOutputFormat.get_options()
        self.assertIsInstance(options, list)
        self.assertTrue(len(options) > 0)

        # Check that separator option exists
        option_names = [opt.name for opt in options]
        self.assertIn('separator', option_names)
        self.assertIn('include_z', option_names)
        self.assertIn('include_header', option_names)
