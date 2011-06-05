import unittest

from totalopenstation.formats.polar import BasePoint, PolarPoint


class TestPolar(unittest.TestCase):

    def setUp(self):
        self.bp0 = BasePoint(x=100.0, y=100.0, z=100.0, ih=0)

        self.p0 = PolarPoint(dist=10,
                             angle=0,
                             z_angle=0,
                             th=0,
                             angle_type='deg',
                             base_point=self.bp0,
                             pid=1,
                             text='Test Point')

    def test_polar(self):
        self.assertEqual(self.p0.to_cartesian(), '100.0,100.0,110.0')
