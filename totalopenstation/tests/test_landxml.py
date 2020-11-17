import unittest

from totalopenstation.formats import Feature, Point
from totalopenstation.formats.landxml import FormatParser
from totalopenstation.output.tops_landxml import OutputFormat

class TestLandXMLParser(unittest.TestCase):

    def setUp(self):
        with open('sample_data/landxml.xml') as testdata:
            self.fp = FormatParser(testdata.read())

    def test_point(self):
        self.assertAlmostEqual(self.fp.points[3].geometry.x, 515.41808873)
        self.assertAlmostEqual(self.fp.points[3].geometry.y, 442.67044336)
        self.assertAlmostEqual(self.fp.points[3].geometry.z, -1.69773328)

    def test_feature(self):
        self.assertEqual(self.fp.points[1].id, 1)
        self.assertEqual(self.fp.points[1].point_name, 'STAZLIB4')
        self.assertEqual(self.fp.points[1].desc, 'PT')
        self.assertEqual(self.fp.points[4].point_name, '902')
        self.assertEqual(self.fp.points[4].desc, 'PT')

    def test_linestring(self):
        self.ls = self.fp.build_linestring()
        self.assertAlmostEqual(self.ls.coords[2][0], 449.72036753)


class TestLandXMLOutput(unittest.TestCase):

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
            Feature(Point(7189.8, 5719.7, 972.6),
                    desc='ST',
                    id=3,
                    point_name='STATION',
                    ih=1.5),
            Feature(Point(6385.4, 4201.6, 943.1),
                    desc='PO',
                    id=4,
                    point_name='TEST POINT #3',
                    z_angle_type='z',
                    dist_type='s',
                    angle=0,
                    z_angle=90.585,
                    dist=1718.28,
                    th=1.5,
                    station_name="STATION")
        ]

    def test_output(self):
        self.output = OutputFormat(self.data).process()
        self.assertEqual(self.output.splitlines()[9], '\t\t\t<CgPoint name="TEST POINT">12.8 76.3 56.2</CgPoint>')
        self.assertEqual(self.output.splitlines()[10], '\t\t\t<CgPoint name="TEST POINT #2">19.8 26.3 46.2</CgPoint>')
        self.assertIn('<InstrumentSetup', self.output.splitlines()[12])
        self.assertIn('id="setup0"', self.output.splitlines()[12])
        self.assertIn('instrumentHeight="1.5"', self.output.splitlines()[12])
        self.assertIn('stationName="STATION"', self.output.splitlines()[12])
        self.assertIn('<RawObservation', self.output.splitlines()[16])
        self.assertIn('targetHeight="1.5"', self.output.splitlines()[16])
        self.assertIn('horizAngle="0"', self.output.splitlines()[16])
        self.assertIn('zenithAngle="90.585"', self.output.splitlines()[16])
        self.assertIn('slopeDistance="1718.28"', self.output.splitlines()[16])
        self.assertEqual(self.output.splitlines()[17], '\t\t\t\t<TargetPoint desc="TEST POINT #3">6385.4 4201.6 943.1</TargetPoint>')
