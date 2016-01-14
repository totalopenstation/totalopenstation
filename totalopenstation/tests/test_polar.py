import unittest

from totalopenstation.formats import Point
from totalopenstation.formats.polar import BasePoint, PolarPoint
from totalopenstation.utils.conversion import deg_to_gon, dms_to_gon


class TestPolar(unittest.TestCase):

    def setUp(self):
        self.bp0 = BasePoint(x='0', y='0', z='0', ih='1.0')
        self.bp1 = BasePoint(x='0', y='0', z='0', ih='1.324')

        self.p0 = PolarPoint(dist=9,
                             angle=deg_to_gon(180),
                             z_angle=deg_to_gon(90),
                             th=0,
                             base_point=self.bp0,
                             pid=1,
                             text='Test Point',
                             coordorder='NEZ')

        self.p1 = PolarPoint(dist=24.567,
                             angle=34.120,
                             z_angle=100,
                             th=1.500,
                             base_point=self.bp0,
                             pid=2,
                             text='Real Point',
                             coordorder='NEZ')

        self.p2 = PolarPoint(dist=13.825,
                             angle=dms_to_gon({"D": '+35',
                                    "M": '45',
                                    "S": '10',
                                    "milliseconds": '0'}),
                             z_angle=dms_to_gon({"D": '+91',
                                      "M": '17',
                                      "S": '51',
                                      "milliseconds": '0'}),
                             th=1.300,
                             base_point=self.bp1,
                             pid=3,
                             text='Real Point',
                             coordorder='NEZ')

    def test_polar(self):
        p0_test = Point(0.0, -9.0, 1.0)
        self.assertAlmostEqual(self.p0.to_point().x, p0_test.x)
        self.assertAlmostEqual(self.p0.to_point().y, p0_test.y)
        self.assertAlmostEqual(self.p0.to_point().z, p0_test.z)

        p1_test = Point(12.5454572076, 21.1222392859, -0.5)
        self.assertAlmostEqual(self.p1.to_point().x, p1_test.x)
        self.assertAlmostEqual(self.p1.to_point().y, p1_test.y)
        self.assertAlmostEqual(self.p1.to_point().z, p1_test.z)

        p2_test = Point(8.0757244, 11.21674196, -0.2890493)
        self.assertAlmostEqual(self.p2.to_point().x, p2_test.x)
        self.assertAlmostEqual(self.p2.to_point().y, p2_test.y)
        self.assertAlmostEqual(self.p2.to_point().z, p2_test.z)
