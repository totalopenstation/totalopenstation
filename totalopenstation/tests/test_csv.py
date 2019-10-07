import unittest

from totalopenstation.formats import Feature, Point
from totalopenstation.output.tops_csv import OutputFormat

class TestCSVOutput(unittest.TestCase):

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
        self.assertEqual(self.output.splitlines()[1], '1,"PT","TEST POINT",12.8,76.3,56.2,"","","","","","",""')
