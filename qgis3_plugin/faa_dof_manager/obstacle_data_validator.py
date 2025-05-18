"""Obstacle data validators"""
from __future__ import annotations

from typing import Any

from .coordinates import dms_to_dd
from .errors import (
    CoordinateError,
    MissingRequiredValueError,
    NumberExpectedError
)


def convert_coordinates(data: dict[str, Any]) -> dict[str, Any] | Exception:
    """Convert coordinates from DMS to DD.

    :param data: obstacle data to be converted
    :return: obstacle data with converted coordinates
    """
    for field, value in data.items():
        try:
            if field == "lon":
                data["lon"] = dms_to_dd(
                    coord=value,
                    max_degree=180
                )
            if field == "lat":
                data["lat"] = dms_to_dd(
                    coord=value,
                    max_degree=90
                )
        except CoordinateError:
            raise CoordinateError(f"Coordinate value error/not supported format: {field}")

    return data



def check_empty(data: dict[str, Any],
                non_empty_fields: list[str]) -> bool | Exception:
    """Check if required fields are not empty.

    :param data: data to be checked
    :param non_empty_fields: fields that values required (not empty)
    :return: obstacle data with checked required fields not empty
    """
    for field, value in data.items():
        if field not in non_empty_fields:
            continue
        if not value:
            raise MissingRequiredValueError(f"Value expected: {field}")

    return True

def cast_to_float(data: dict[str, Any],
                  to_float_fields: list[str]) -> bool | Exception:
    """Convert numeric fields from strings to numbers.

    :param data: data to be checked
    :param to_float_fields: field names that are need to be converted to number
    :return: obstacle data with numeric fields converted to numbers
    """
    for field, value in data.items():
        if field not in to_float_fields:
            continue
        try:
            data[field] = float(value)
        except ValueError:
            raise NumberExpectedError(f"Number expected: {field}")

    return True


def validate_obstacle(data: dict[str, Any]) -> dict[str, str] | Exception:
    """Validate obstacle data taken from plugin GUI.

    :param data: data to be checked
    :return:
    """
    try:
        convert_coordinates(data=data)
        check_empty(
            data=data,
            non_empty_fields=[
                "obst_number",
                "city"
            ]
        )
        cast_to_float(
            data=data,
            to_float_fields=[
                "agl",
                "amsl",
                "quantity"
            ]
        )
    except (MissingRequiredValueError, NumberExpectedError, CoordinateError) as e:
        raise ValueError(e) from e

    return data
