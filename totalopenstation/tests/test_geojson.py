import json
import unittest

from totalopenstation.formats import Feature, FeatureCollection, Point
from totalopenstation.output.tops_geojson import OutputFormat

class TestGeoJSONOutput(unittest.TestCase):

    def setUp(self):
        self.data = FeatureCollection([
            Feature(Point(12.8, 76.3, 56.2),
                    desc='TEST POINT',
                    id=1),
            Feature(Point(19.8, 26.3, 46.2),
                    desc='TEST POINT #2',
                    id=2),
        ])

    def test_output(self):
        self.output = OutputFormat(self.data).process()
        self.assertEqual(self.output, '''{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [12.8, 76.3, 56.2]}, "type": "Feature", "properties": {"desc": "TEST POINT"}, "id": 1}, {"geometry": {"type": "Point", "coordinates": [19.8, 26.3, 46.2]}, "type": "Feature", "properties": {"desc": "TEST POINT #2"}, "id": 2}]}''')
