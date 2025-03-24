import json
import unittest

from totalopenstation.formats import Feature, FeatureCollection, Point
from totalopenstation.output.tops_geojson import OutputFormat

class TestGeoJSONOutput(unittest.TestCase):

    def setUp(self):
        self.data = [
            Feature(Point(12.8, 76.3, 56.2),
                    desc='TEST POINT',
                    id=1),
            Feature(Point(19.8, 26.3, 46.2),
                    desc='TEST POINT #2',
                    id=2),
        ]

    def test_output(self):
        self.maxDiff = None
        self.output = OutputFormat(self.data).process()
        ref_output = '''{"type": "FeatureCollection", "bbox": [12.8, 26.3, 19.8, 76.3], "features": [{"type": "Feature", "bbox": [12.8, 76.3, 12.8, 76.3], "geometry": {"type": "Point", "bbox": [12.8, 76.3, 12.8, 76.3], "coordinates": [12.8, 76.3, 56.2]}, "properties": {"desc": "TEST POINT"}, "id": 1}, {"type": "Feature", "bbox": [19.8, 26.3, 19.8, 26.3], "geometry": {"type": "Point", "bbox": [19.8, 26.3, 19.8, 26.3], "coordinates": [19.8, 26.3, 46.2]}, "properties": {"desc": "TEST POINT #2"}, "id": 2}]}'''
        self.assertEqual(json.loads(self.output), json.loads(ref_output))
