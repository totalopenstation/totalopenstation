import unittest

from totalopenstation.formats.detect import (
    detect_format,
    get_format_description,
    list_detectable_formats,
)


class TestFormatDetection(unittest.TestCase):

    def test_detect_landxml(self):
        """Test detection of LandXML format."""
        data = '''<LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2">
            <Survey><CgPoints></CgPoints></Survey>
        </LandXML>'''
        self.assertEqual(detect_format(data), 'landxml')

    def test_detect_leica_gsi(self):
        """Test detection of Leica GSI format."""
        data = '*110001+00000001 21.322+03496940 22.322+09364360 31..00+00030485'
        self.assertEqual(detect_format(data), 'leica_gsi')

    def test_detect_sokkia_sdr33(self):
        """Test detection of Sokkia SDR33 format."""
        data = '''00NMSDR33 V04-04.02     00-000-00 00:00 211111
10NMJOB3            121111
02TP        00000031509.97000000    937.27400000'''
        self.assertEqual(detect_format(data), 'sokkia_sdr33')

    def test_detect_carlson_rw5(self):
        """Test detection of Carlson RW5 format."""
        data = '''-- TPS1200 RW5 format file
JB,NMMY RW5 JOB,DT07-22-2004,TM13:13:51
MO,AD0,UN0,SF1.00000000,EC1,EO0.0,AU0'''
        self.assertEqual(detect_format(data), 'carlson_rw5')

    def test_detect_topcon_gts(self):
        """Test detection of Topcon GTS format."""
        data = "1.500_+1_ ?+00043575m0970930+1317260g+00043530t**+00+00111"
        self.assertEqual(detect_format(data), 'topcon_gts')

    def test_detect_tops_marker(self):
        """Test detection using TOPS format marker."""
        data = '''# -*- tops-format: zeiss_r5 -*-
Some data here...'''
        self.assertEqual(detect_format(data), 'zeiss_r5')

    def test_detect_unknown_format(self):
        """Test that unknown format returns None."""
        data = "random gibberish that doesn't match any format"
        self.assertIsNone(detect_format(data))

    def test_return_all_matches(self):
        """Test returning all matching formats with scores."""
        data = '<LandXML xmlns="http://www.landxml.org/schema/LandXML-1.2"></LandXML>'
        matches = detect_format(data, return_all=True)
        self.assertIsInstance(matches, list)
        self.assertTrue(len(matches) > 0)
        self.assertEqual(matches[0][0], 'landxml')

    def test_get_format_description(self):
        """Test getting format description."""
        desc = get_format_description('landxml')
        self.assertIn('XML', desc)

    def test_list_detectable_formats(self):
        """Test listing detectable formats."""
        formats = list_detectable_formats()
        self.assertIsInstance(formats, list)
        self.assertTrue(len(formats) > 0)
        # Check that each entry is a tuple of (name, description)
        for name, desc in formats:
            self.assertIsInstance(name, str)
            self.assertIsInstance(desc, str)
