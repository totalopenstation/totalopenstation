import json
import unittest

from totalopenstation.formats import FeatureCollection, Point
from totalopenstation.output.tops_geojson import OutputFormat

from pygeoif.geometry import Feature

class TestGeoJSONOutput(unittest.TestCase):

    def setUp(self):
        self.data = FeatureCollection([
            Feature(geometry=Point(12.8, 76.3, 56.2),
                    properties={'desc': 'TEST POINT'},
                    feature_id=1),
            Feature(geometry=Point(19.8, 26.3, 46.2),
                    properties={'desc': 'TEST POINT #2'},
                    feature_id=2),
        ])

    def test_output(self):
        self.output = OutputFormat(self.data).process()
        self.assertEqual(self.output, '''{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [12.8, 76.3, 56.2]}, "type": "Feature", "properties": {"desc": "TEST POINT"}, "id": 1}, {"geometry": {"type": "Point", "coordinates": [19.8, 26.3, 46.2]}, "type": "Feature", "properties": {"desc": "TEST POINT #2"}, "id": 2}]}''')
