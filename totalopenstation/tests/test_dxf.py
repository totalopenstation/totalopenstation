import unittest

from totalopenstation.formats import Feature, LineString, Point
from totalopenstation.output.tops_dxf import OutputFormat

class TestCSVOutput(unittest.TestCase):

    def setUp(self):
        self.data = [
            Feature(geometry=Point(12.8, 76.3, 56.2),
                    desc='TESTPOINT',
                    id=1),
            Feature(geometry=Point(19.8, 26.3, 46.2),
                    desc='TESTPOINT2',
                    id=2),
            Feature(geometry=LineString(((17.8, 26.0, 41.2),
                                         (18.8, 26.6, 44.2),
                                         (24.8, 26.9, 42.2))),
                    desc='TESTLINE',
                    id=3),
        ]

    def test_output(self):
        self.output = OutputFormat(self.data, separate_layers=False).process()
        with open('/home/steko/test.dxf', 'wb') as f:
            f.write(self.output)
        #self.assertEqual(self.output.splitlines()[1], '1,12.8,76.3,56.2,"TEST POINT"')
