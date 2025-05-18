"""Coordinate conversion"""
from __future__ import annotations

from .errors import CoordinateError

HEMISPHERES = ["N", "S", "W", "E"]
NEGATIVE_SIGN = ["S", "W"]


def dms_to_dd(coord: str,
              max_degree: int) -> float | Exception:
    """Convert coordinate from DMS (degree, minutes, second) to DD (decimal degrees) format.

    :param coord: coordinate value to be converted
    :param max_degree: maximum degree value for coordinates:
        90 for longitude
        180 for latitude
    :return: coordinate in decimal degree format/value
    """
    h = coord[-1]
    if h not in HEMISPHERES:
        raise CoordinateError

    try:
        d, m, s = coord[:-1].split("-")
        d = int(d)
        m = int(m)
        s = float(s)
    except Exception as e:
        raise CoordinateError from e

    if (
            not 0 <= d <= max_degree
            or not 0 <= m < 60
            or not 0 <= s < 60
            or d == max_degree and (m != 0 or s != 0)
    ):
        raise CoordinateError

    dd = d + m / 60 + s / 3600
    if h in NEGATIVE_SIGN:
        return -dd
    return dd
