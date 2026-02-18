# -*- coding: utf-8 -*-
# filename: celerimetry.py
# Copyright 2026 Enzo Cocca <enzo.ccc@gmail.com>
#
# This file is part of Total Open Station.
#
# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Total Open Station is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.

"""
Celerimetric calculation module for Total Open Station.

This module provides functions and classes for computing coordinates
from polar measurements (angles and distances) using standard
topographic/surveying formulas.

Terminology:
- Station: The point where the total station is set up
- Backsight/Orientation: A known point used to orient the instrument
- Foresight: Points being measured from the station
- Hz: Horizontal angle (azimuth reading on the instrument)
- V: Vertical/Zenith angle (90° = horizontal, <90° = upward, >90° = downward)
- Slope distance: The measured distance along the line of sight
"""

import math
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict

logger = logging.getLogger(__name__)


@dataclass
class Point3D:
    """A point with 3D coordinates and optional metadata."""
    x: float  # Easting
    y: float  # Northing
    z: float  # Elevation
    name: str = ""
    code: str = ""

    def distance_to(self, other: 'Point3D') -> float:
        """Calculate 3D distance to another point."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def horizontal_distance_to(self, other: 'Point3D') -> float:
        """Calculate 2D horizontal distance to another point."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )

    def azimuth_to(self, other: 'Point3D') -> float:
        """
        Calculate azimuth from this point to another point.

        Returns:
            Azimuth in decimal degrees (0-360), measured clockwise from North.
        """
        delta_e = other.x - self.x
        delta_n = other.y - self.y

        azimuth_rad = math.atan2(delta_e, delta_n)
        azimuth_deg = math.degrees(azimuth_rad)

        # Normalize to 0-360
        if azimuth_deg < 0:
            azimuth_deg += 360

        return azimuth_deg


@dataclass
class PolarObservation:
    """A polar observation (measurement) from a total station."""
    hz_angle: float  # Horizontal angle in decimal degrees
    v_angle: float   # Vertical/zenith angle in decimal degrees
    slope_dist: float  # Slope distance in meters
    target_height: float = 0.0  # Prism/target height
    point_name: str = ""
    code: str = ""
    prism_constant: float = 0.0  # Prism constant in meters (usually negative)

    @property
    def corrected_distance(self) -> float:
        """Return slope distance corrected for prism constant."""
        return self.slope_dist + self.prism_constant

    @property
    def horizontal_distance(self) -> float:
        """Calculate horizontal distance from slope distance and vertical angle."""
        # V angle: 90° = horizontal, <90° = looking up, >90° = looking down
        v_rad = math.radians(self.v_angle)
        return self.corrected_distance * math.sin(v_rad)

    @property
    def vertical_difference(self) -> float:
        """Calculate vertical difference (delta Z) from slope distance and vertical angle."""
        v_rad = math.radians(self.v_angle)
        return self.corrected_distance * math.cos(v_rad)


@dataclass
class StationSetup:
    """A station setup with instrument position and orientation."""
    station: Point3D
    instrument_height: float
    backsight: Optional[Point3D] = None
    backsight_hz_reading: float = 0.0  # Hz reading when pointing to backsight

    @property
    def orientation_azimuth(self) -> Optional[float]:
        """
        Calculate the azimuth correction (orientation).

        This is the difference between the true azimuth to the backsight
        and the horizontal circle reading when pointing to the backsight.
        """
        if self.backsight is None:
            return None

        true_azimuth = self.station.azimuth_to(self.backsight)
        return true_azimuth - self.backsight_hz_reading


class CelerimetricCalculator:
    """
    Calculator for celerimetric (tacheometric) computations.

    This class computes coordinates from polar observations using
    standard surveying formulas.

    Example usage:
        >>> station = Point3D(x=374339.863, y=4128109.811, z=64.628, name="200")
        >>> backsight = Point3D(x=374299.819, y=4128118.709, z=63.194, name="300")
        >>>
        >>> calc = CelerimetricCalculator()
        >>> calc.set_station(station, instrument_height=1.635)
        >>> calc.set_backsight(backsight, hz_reading=167.456)
        >>>
        >>> obs = PolarObservation(hz_angle=223.056, v_angle=92.668, slope_dist=36.778)
        >>> point = calc.compute_point(obs)
        >>> print(f"X={point.x:.3f}, Y={point.y:.3f}, Z={point.z:.3f}")
    """

    def __init__(self):
        self.station_setup: Optional[StationSetup] = None
        self.observations: List[PolarObservation] = []
        self.computed_points: List[Point3D] = []

    def set_station(self, station: Point3D, instrument_height: float = 0.0):
        """
        Set the station point.

        Args:
            station: The station point with known coordinates
            instrument_height: Height of the instrument above the station point
        """
        self.station_setup = StationSetup(
            station=station,
            instrument_height=instrument_height
        )
        logger.info(f"Station set: {station.name} at ({station.x:.3f}, {station.y:.3f}, {station.z:.3f})")

    def set_backsight(self, backsight: Point3D, hz_reading: float):
        """
        Set the backsight point for orientation.

        Args:
            backsight: The backsight point with known coordinates
            hz_reading: The horizontal circle reading when pointing to backsight
        """
        if self.station_setup is None:
            raise ValueError("Station must be set before backsight")

        self.station_setup.backsight = backsight
        self.station_setup.backsight_hz_reading = hz_reading

        orientation = self.station_setup.orientation_azimuth
        true_az = self.station_setup.station.azimuth_to(backsight)

        logger.info(f"Backsight set: {backsight.name}")
        logger.info(f"  True azimuth to backsight: {true_az:.4f}°")
        logger.info(f"  Hz reading at backsight: {hz_reading:.4f}°")
        logger.info(f"  Orientation correction: {orientation:.4f}°")

    def compute_azimuth(self, hz_reading: float) -> float:
        """
        Compute the true azimuth from a horizontal circle reading.

        Args:
            hz_reading: The horizontal circle reading in decimal degrees

        Returns:
            True azimuth in decimal degrees (0-360)
        """
        if self.station_setup is None:
            raise ValueError("Station must be set")

        orientation = self.station_setup.orientation_azimuth
        if orientation is None:
            # No backsight - assume instrument is oriented to north
            logger.warning("No backsight set - assuming Hz reading equals azimuth")
            return hz_reading % 360

        azimuth = hz_reading + orientation

        # Normalize to 0-360
        while azimuth < 0:
            azimuth += 360
        while azimuth >= 360:
            azimuth -= 360

        return azimuth

    def compute_point(self, observation: PolarObservation) -> Point3D:
        """
        Compute coordinates for a point from a polar observation.

        Args:
            observation: The polar observation (Hz, V, distance)

        Returns:
            Point3D with computed coordinates
        """
        if self.station_setup is None:
            raise ValueError("Station must be set")

        station = self.station_setup.station
        inst_height = self.station_setup.instrument_height

        # Compute true azimuth
        azimuth = self.compute_azimuth(observation.hz_angle)
        azimuth_rad = math.radians(azimuth)

        # Compute horizontal distance
        horiz_dist = observation.horizontal_distance

        # Compute delta E and delta N
        delta_e = horiz_dist * math.sin(azimuth_rad)
        delta_n = horiz_dist * math.cos(azimuth_rad)

        # Compute coordinates
        x = station.x + delta_e
        y = station.y + delta_n

        # Compute elevation
        # Z = Station_Z + Instrument_Height + Vertical_Difference - Target_Height
        z = station.z + inst_height + observation.vertical_difference - observation.target_height

        point = Point3D(
            x=x, y=y, z=z,
            name=observation.point_name,
            code=observation.code
        )

        logger.debug(f"Computed {observation.point_name}: "
                    f"Az={azimuth:.4f}°, HDist={horiz_dist:.3f}m -> "
                    f"({x:.3f}, {y:.3f}, {z:.3f})")

        return point

    def add_observation(self, observation: PolarObservation) -> Point3D:
        """
        Add an observation and compute its coordinates.

        Args:
            observation: The polar observation

        Returns:
            The computed point
        """
        self.observations.append(observation)
        point = self.compute_point(observation)
        self.computed_points.append(point)
        return point

    def compute_all(self, observations: List[PolarObservation]) -> List[Point3D]:
        """
        Compute coordinates for multiple observations.

        Args:
            observations: List of polar observations

        Returns:
            List of computed points
        """
        points = []
        for obs in observations:
            point = self.add_observation(obs)
            points.append(point)
        return points

    def get_computation_report(self) -> str:
        """Generate a report of the celerimetric computation."""
        lines = []
        lines.append("=" * 70)
        lines.append("CELERIMETRIC COMPUTATION REPORT")
        lines.append("=" * 70)

        if self.station_setup:
            st = self.station_setup.station
            lines.append(f"\nStation: {st.name}")
            lines.append(f"  Coordinates: E={st.x:.3f}, N={st.y:.3f}, Z={st.z:.3f}")
            lines.append(f"  Instrument height: {self.station_setup.instrument_height:.3f} m")

            if self.station_setup.backsight:
                bs = self.station_setup.backsight
                lines.append(f"\nBacksight: {bs.name}")
                lines.append(f"  Coordinates: E={bs.x:.3f}, N={bs.y:.3f}, Z={bs.z:.3f}")
                lines.append(f"  Hz reading: {self.station_setup.backsight_hz_reading:.4f}°")
                lines.append(f"  True azimuth: {st.azimuth_to(bs):.4f}°")
                lines.append(f"  Orientation: {self.station_setup.orientation_azimuth:.4f}°")

        if self.computed_points:
            lines.append(f"\nComputed Points ({len(self.computed_points)}):")
            lines.append("-" * 70)
            lines.append(f"{'Name':<12} {'Easting':>14} {'Northing':>14} {'Elevation':>12} {'Code':<10}")
            lines.append("-" * 70)

            for p in self.computed_points:
                lines.append(f"{p.name:<12} {p.x:>14.3f} {p.y:>14.3f} {p.z:>12.3f} {p.code:<10}")

        lines.append("=" * 70)
        return "\n".join(lines)


def degrees_to_decimal(degrees: float, minutes: float = 0, seconds: float = 0) -> float:
    """
    Convert degrees, minutes, seconds to decimal degrees.

    Args:
        degrees: Degrees (integer part)
        minutes: Minutes (0-59)
        seconds: Seconds (0-59.999...)

    Returns:
        Decimal degrees
    """
    sign = 1 if degrees >= 0 else -1
    return sign * (abs(degrees) + minutes / 60 + seconds / 3600)


def decimal_to_dms(decimal_degrees: float) -> Tuple[int, int, float]:
    """
    Convert decimal degrees to degrees, minutes, seconds.

    Args:
        decimal_degrees: Angle in decimal degrees

    Returns:
        Tuple of (degrees, minutes, seconds)
    """
    sign = 1 if decimal_degrees >= 0 else -1
    dd = abs(decimal_degrees)

    degrees = int(dd)
    minutes_float = (dd - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60

    return (sign * degrees, minutes, seconds)


def gon_to_degrees(gon: float) -> float:
    """Convert gradians (gon) to decimal degrees."""
    return gon * 0.9  # 400 gon = 360 degrees


def degrees_to_gon(degrees: float) -> float:
    """Convert decimal degrees to gradians (gon)."""
    return degrees / 0.9


def compute_azimuth(from_point: Tuple[float, float],
                    to_point: Tuple[float, float]) -> float:
    """
    Compute azimuth between two points.

    Args:
        from_point: (x, y) tuple of starting point (Easting, Northing)
        to_point: (x, y) tuple of target point

    Returns:
        Azimuth in decimal degrees (0-360), clockwise from North
    """
    delta_e = to_point[0] - from_point[0]
    delta_n = to_point[1] - from_point[1]

    azimuth_rad = math.atan2(delta_e, delta_n)
    azimuth_deg = math.degrees(azimuth_rad)

    if azimuth_deg < 0:
        azimuth_deg += 360

    return azimuth_deg


def polar_to_cartesian(station: Tuple[float, float, float],
                       azimuth: float,
                       horiz_distance: float,
                       delta_z: float = 0.0) -> Tuple[float, float, float]:
    """
    Convert polar coordinates to cartesian coordinates.

    Args:
        station: (x, y, z) of the station point
        azimuth: Azimuth in decimal degrees (0-360, clockwise from North)
        horiz_distance: Horizontal distance in meters
        delta_z: Vertical difference (can include instrument/target heights)

    Returns:
        (x, y, z) tuple of the computed point
    """
    az_rad = math.radians(azimuth)

    delta_e = horiz_distance * math.sin(az_rad)
    delta_n = horiz_distance * math.cos(az_rad)

    x = station[0] + delta_e
    y = station[1] + delta_n
    z = station[2] + delta_z

    return (x, y, z)
