# -*- coding: utf-8 -*-
# Tests for celerimetry module

import unittest
import math
from totalopenstation.utils.celerimetry import (
    Point3D,
    PolarObservation,
    CelerimetricCalculator,
    compute_azimuth,
    polar_to_cartesian,
    degrees_to_decimal,
    decimal_to_dms,
    gon_to_degrees,
    degrees_to_gon,
)


class TestPoint3D(unittest.TestCase):
    """Tests for Point3D class."""

    def test_distance_to(self):
        """Test 3D distance calculation."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=3, y=4, z=0)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0, places=6)

    def test_horizontal_distance_to(self):
        """Test 2D horizontal distance calculation."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=3, y=4, z=10)  # Z doesn't matter
        self.assertAlmostEqual(p1.horizontal_distance_to(p2), 5.0, places=6)

    def test_azimuth_to_north(self):
        """Test azimuth calculation - due north."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=0, y=100, z=0)  # Due north
        self.assertAlmostEqual(p1.azimuth_to(p2), 0.0, places=6)

    def test_azimuth_to_east(self):
        """Test azimuth calculation - due east."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=100, y=0, z=0)  # Due east
        self.assertAlmostEqual(p1.azimuth_to(p2), 90.0, places=6)

    def test_azimuth_to_south(self):
        """Test azimuth calculation - due south."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=0, y=-100, z=0)  # Due south
        self.assertAlmostEqual(p1.azimuth_to(p2), 180.0, places=6)

    def test_azimuth_to_west(self):
        """Test azimuth calculation - due west."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=-100, y=0, z=0)  # Due west
        self.assertAlmostEqual(p1.azimuth_to(p2), 270.0, places=6)

    def test_azimuth_to_northeast(self):
        """Test azimuth calculation - 45 degrees (NE)."""
        p1 = Point3D(x=0, y=0, z=0)
        p2 = Point3D(x=100, y=100, z=0)  # 45 degrees
        self.assertAlmostEqual(p1.azimuth_to(p2), 45.0, places=6)


class TestPolarObservation(unittest.TestCase):
    """Tests for PolarObservation class."""

    def test_horizontal_distance(self):
        """Test horizontal distance calculation from slope distance."""
        # Horizontal shot (V=90°)
        obs = PolarObservation(hz_angle=0, v_angle=90.0, slope_dist=100.0)
        self.assertAlmostEqual(obs.horizontal_distance, 100.0, places=6)

        # 45° downward shot (V=135°)
        obs2 = PolarObservation(hz_angle=0, v_angle=135.0, slope_dist=100.0)
        self.assertAlmostEqual(obs2.horizontal_distance, 100 * math.sin(math.radians(135)), places=6)

    def test_vertical_difference(self):
        """Test vertical difference calculation."""
        # Horizontal shot - no vertical difference
        obs = PolarObservation(hz_angle=0, v_angle=90.0, slope_dist=100.0)
        self.assertAlmostEqual(obs.vertical_difference, 0.0, places=5)

        # Looking up at 45° (V=45°)
        obs2 = PolarObservation(hz_angle=0, v_angle=45.0, slope_dist=100.0)
        expected = 100 * math.cos(math.radians(45))  # ~70.71
        self.assertAlmostEqual(obs2.vertical_difference, expected, places=5)

    def test_prism_constant(self):
        """Test prism constant correction."""
        obs = PolarObservation(hz_angle=0, v_angle=90.0, slope_dist=100.0, prism_constant=-0.030)
        self.assertAlmostEqual(obs.corrected_distance, 99.970, places=6)


class TestCelerimetricCalculator(unittest.TestCase):
    """Tests for CelerimetricCalculator class."""

    def setUp(self):
        """Set up test data based on real Agrigento survey."""
        # Station 200
        self.station = Point3D(
            x=374339.863, y=4128109.811, z=64.628, name="200"
        )
        # Backsight 300
        self.backsight = Point3D(
            x=374299.819, y=4128118.709, z=63.194, name="300"
        )
        self.instrument_height = 1.635
        self.backsight_hz = 167.456  # Hz reading when pointing to 300

    def test_station_setup(self):
        """Test station setup."""
        calc = CelerimetricCalculator()
        calc.set_station(self.station, self.instrument_height)
        self.assertEqual(calc.station_setup.station.name, "200")
        self.assertEqual(calc.station_setup.instrument_height, 1.635)

    def test_backsight_orientation(self):
        """Test backsight orientation calculation."""
        calc = CelerimetricCalculator()
        calc.set_station(self.station, self.instrument_height)
        calc.set_backsight(self.backsight, self.backsight_hz)

        # Calculate expected true azimuth from station to backsight
        true_az = self.station.azimuth_to(self.backsight)
        orientation = calc.station_setup.orientation_azimuth

        # Orientation should be: true_azimuth - hz_reading
        expected_orientation = true_az - self.backsight_hz
        self.assertAlmostEqual(orientation, expected_orientation, places=4)

    def test_compute_azimuth(self):
        """Test azimuth computation with orientation correction."""
        calc = CelerimetricCalculator()
        calc.set_station(self.station, self.instrument_height)
        calc.set_backsight(self.backsight, self.backsight_hz)

        # Azimuth for backsight reading should equal true azimuth to backsight
        true_az = self.station.azimuth_to(self.backsight)
        computed_az = calc.compute_azimuth(self.backsight_hz)
        self.assertAlmostEqual(computed_az, true_az, places=4)

    def test_compute_point_horizontal(self):
        """Test point computation for horizontal shot."""
        calc = CelerimetricCalculator()
        calc.set_station(self.station, self.instrument_height)
        calc.set_backsight(self.backsight, self.backsight_hz)

        # Create observation: due north, 100m horizontal
        # Need to find Hz reading that gives due north
        orientation = calc.station_setup.orientation_azimuth
        hz_for_north = (0 - orientation) % 360

        obs = PolarObservation(
            hz_angle=hz_for_north,
            v_angle=90.0,  # Horizontal
            slope_dist=100.0,
            target_height=self.instrument_height,
            point_name="TEST"
        )

        point = calc.compute_point(obs)

        # Point should be 100m north of station
        self.assertAlmostEqual(point.x, self.station.x, places=2)
        self.assertAlmostEqual(point.y, self.station.y + 100, places=2)


class TestConversionFunctions(unittest.TestCase):
    """Tests for angle conversion functions."""

    def test_degrees_to_decimal(self):
        """Test DMS to decimal conversion."""
        # 45° 30' 30"
        result = degrees_to_decimal(45, 30, 30)
        expected = 45 + 30/60 + 30/3600
        self.assertAlmostEqual(result, expected, places=6)

    def test_decimal_to_dms(self):
        """Test decimal to DMS conversion."""
        decimal = 45.5083333  # 45° 30' 30"
        d, m, s = decimal_to_dms(decimal)
        self.assertEqual(d, 45)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 30.0, places=1)

    def test_gon_to_degrees(self):
        """Test gradians to degrees conversion."""
        self.assertAlmostEqual(gon_to_degrees(100), 90.0, places=6)
        self.assertAlmostEqual(gon_to_degrees(200), 180.0, places=6)
        self.assertAlmostEqual(gon_to_degrees(400), 360.0, places=6)

    def test_degrees_to_gon(self):
        """Test degrees to gradians conversion."""
        self.assertAlmostEqual(degrees_to_gon(90), 100.0, places=6)
        self.assertAlmostEqual(degrees_to_gon(180), 200.0, places=6)
        self.assertAlmostEqual(degrees_to_gon(360), 400.0, places=6)


class TestStandaloneFunctions(unittest.TestCase):
    """Tests for standalone calculation functions."""

    def test_compute_azimuth(self):
        """Test azimuth computation function."""
        # Due north
        az = compute_azimuth((0, 0), (0, 100))
        self.assertAlmostEqual(az, 0.0, places=6)

        # Due east
        az = compute_azimuth((0, 0), (100, 0))
        self.assertAlmostEqual(az, 90.0, places=6)

    def test_polar_to_cartesian(self):
        """Test polar to cartesian conversion."""
        station = (1000.0, 2000.0, 100.0)

        # Due north, 100m
        x, y, z = polar_to_cartesian(station, azimuth=0.0, horiz_distance=100.0)
        self.assertAlmostEqual(x, 1000.0, places=3)
        self.assertAlmostEqual(y, 2100.0, places=3)
        self.assertAlmostEqual(z, 100.0, places=3)

        # Due east, 100m
        x, y, z = polar_to_cartesian(station, azimuth=90.0, horiz_distance=100.0)
        self.assertAlmostEqual(x, 1100.0, places=3)
        self.assertAlmostEqual(y, 2000.0, places=3)


if __name__ == '__main__':
    unittest.main()
