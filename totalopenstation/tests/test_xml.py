import unittest

from totalopenstation.formats import Feature, Point
from totalopenstation.output.tops_xml import OutputFormat

class TestXMLOutput(unittest.TestCase):

    def setUp(self):
        self.data = [
            Feature(Point(12.8, 76.3, 56.2),
                    desc='PT',
                    point_name='TEST POINT',
                    id=1),
            Feature(Point(19.8, 26.3, 46.2),
                    desc='PT',
                    point_name='TEST POINT #2',
                    id=2),
        ]

    def test_output(self):
        self.output = OutputFormat(self.data).process()
        self.assertEqual(self.output.splitlines()[9], b'\t\t\t<CgPoint name="TEST POINT">12.8 76.3 56.2</CgPoint>')
        self.assertEqual(self.output.splitlines()[10], b'\t\t\t<CgPoint name="TEST POINT #2">19.8 26.3 46.2</CgPoint>')
