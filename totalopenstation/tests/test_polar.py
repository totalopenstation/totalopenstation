import unittest

from totalopenstation.formats import Point
from totalopenstation.formats.polar import BasePoint, PolarPoint


class TestPolar(unittest.TestCase):

    def setUp(self):
        self.bp0 = BasePoint(x='0', y='0', z='0', ih='1.0')

        self.p0 = PolarPoint(dist=9,
                             angle=180,
                             z_angle=90,
                             th=0,
                             angle_type='deg',
                             base_point=self.bp0,
                             pid=1,
                             text='Test Point',
                             coordorder='NEZ')

        self.p1 = PolarPoint(dist=24.567,
                             angle=34.120,
                             z_angle=100,
                             th=1.500,
                             angle_type='gon',
                             base_point=self.bp0,
                             pid=2,
                             text='Real Point',
                             coordorder='NEZ')

    def test_polar(self):

        for i, j in zip(self.p0.to_point().tuplepoint,
                        Point(1, 0.0, -9.0, 1.0, 'Test Point').tuplepoint):
            self.assertAlmostEqual(i, j)

        for i, j in zip(self.p1.to_point().tuplepoint,
                     Point(2, 12.5454572076, 21.1222392859, -0.5, 'Real Point').tuplepoint):
            self.assertAlmostEqual(i, j)
