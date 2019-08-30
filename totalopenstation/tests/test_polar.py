import unittest

from totalopenstation.formats import Point
from totalopenstation.formats.polar import BasePoint, PolarPoint


class TestPolar(unittest.TestCase):

    def setUp(self):
        self.bp0 = BasePoint(x='0', y='0', z='0', ih='1.0', b_zero_st='0.0')
        self.bp1 = BasePoint(x='0', y='0', z='0', ih='1.324', b_zero_st='0.0')

        self.p0 = PolarPoint(angle_unit='deg',
                             z_angle_type='z',
                             dist_type='s',
                             dist=9,
                             angle=180,
                             z_angle=90,
                             th=0,
                             base_point=self.bp0,
                             pid=1,
                             text='Test Point',
                             coordorder='ENZ')

        self.p1 = PolarPoint(angle_unit='gon',
                             z_angle_type='z',
                             dist_type='s',
                             dist=24.567,
                             angle=34.120,
                             z_angle=100,
                             th=1.500,
                             base_point=self.bp0,
                             pid=2,
                             text='Real Point',
                             coordorder='NEZ')

        self.p2 = PolarPoint(angle_unit='dms',
                             z_angle_type='z',
                             dist_type='s',
                             dist=13.825,
                             angle=35.45100,
                             z_angle=91.17510,
                             th=1.300,
                             base_point=self.bp1,
                             pid=3,
                             text='Real Point',
                             coordorder='ENZ')

    def test_polar(self):
        p0_test = Point(0.0, -9.0, 1.0)
        self.assertAlmostEqual(self.p0.to_point().x, p0_test.x)
        self.assertAlmostEqual(self.p0.to_point().y, p0_test.y)
        self.assertAlmostEqual(self.p0.to_point().z, p0_test.z)

        p1_test = Point(21.1222392859, 12.5454572076, -0.5)
        self.assertAlmostEqual(self.p1.to_point().x, p1_test.x)
        self.assertAlmostEqual(self.p1.to_point().y, p1_test.y)
        self.assertAlmostEqual(self.p1.to_point().z, p1_test.z)

        p2_test = Point(8.0757244, 11.21674196, -0.2890493)
        self.assertAlmostEqual(self.p2.to_point().x, p2_test.x)
        self.assertAlmostEqual(self.p2.to_point().y, p2_test.y)
        self.assertAlmostEqual(self.p2.to_point().z, p2_test.z)
