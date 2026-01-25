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
        result = json.loads(self.output)

        # Verify structure
        self.assertEqual(result['type'], 'FeatureCollection')
        self.assertIn('features', result)
        self.assertEqual(len(result['features']), 2)

        # Verify first feature
        f1 = result['features'][0]
        self.assertEqual(f1['type'], 'Feature')
        self.assertEqual(f1['id'], 1)
        self.assertEqual(f1['properties']['desc'], 'TEST POINT')
        self.assertEqual(f1['geometry']['type'], 'Point')
        self.assertEqual(f1['geometry']['coordinates'], [12.8, 76.3, 56.2])

        # Verify second feature
        f2 = result['features'][1]
        self.assertEqual(f2['type'], 'Feature')
        self.assertEqual(f2['id'], 2)
        self.assertEqual(f2['properties']['desc'], 'TEST POINT #2')
        self.assertEqual(f2['geometry']['type'], 'Point')
        self.assertEqual(f2['geometry']['coordinates'], [19.8, 26.3, 46.2])
