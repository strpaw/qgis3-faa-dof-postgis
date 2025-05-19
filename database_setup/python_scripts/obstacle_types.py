"""Parse DOF file to fetch unique obstacle types"""
from __future__ import annotations
from dataclasses import dataclass

from dacite import (
    from_dict,
    MissingValueError,
    WrongTypeError
)
import pandas as pd
from yaml import safe_load


@dataclass(frozen=True)
class ObstTypeField:
    """Obstacle type data element"""
    start: int
    end: int


@dataclass(frozen=True)
class Configuration:
    """Script configuration"""
    skip_rows: int
    encoding: str
    obst_type_field: ObstTypeField

    @classmethod
    def from_file(cls, path: str) -> Configuration | None:
        """Create instance of configuration class based on configuration file content

        :param path: path to the configuration file
        :return: instance of Configuration class, or None if exception risen
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = safe_load(f)
                return from_dict(
                    data_class=Configuration,
                    data=content
                )
        except FileNotFoundError as e:
            print(e)
            return None
        except (MissingValueError, WrongTypeError) as e:
            print(f"Config file error: {e}")
            return None


def get_obstacle_types(
        file_path: str,
        skip_rows: int,
        start_column: int,
        end_column: int,
        encoding: str
) -> pd.Series:
    """Return unique obstacle types based on the Digital Obstacle File (DOF).

    :param file_path: path to the DOF
    :param skip_rows: Number of rows to skip (header rows without actual obstacle data)
    :param start_column: number of the column where obstacle type begins
    :param end_column: number of the column where obstacle type ends
    :param encoding: DOF encoding
    :return: Unique obstacle types
    """
    df = pd.read_fwf(
        file_path,
        skiprows=skip_rows,
        header=None,
        colspecs=[(start_column, end_column)],
        names=["type"],
        encoding=encoding
    )

    types = pd.DataFrame(
        df["type"].unique(),
        columns=["type"]
    )

    types.sort_values(
        by=["type"],
        axis=0,
        inplace=True
    )

    return types.type.str.strip()


def main():
    """Main loop"""
    config = Configuration.from_file("obstacle_types_config.yml")

    obst_types = get_obstacle_types(
        file_path="DOF.dat",
        skip_rows=config.skip_rows,
        start_column=config.obst_type_field.start,
        end_column=config.obst_type_field.end,
        encoding=config.encoding
    )
    obst_types.to_csv(
        "obstacle_types.csv",
        index=False
    )


if __name__ == "__main__":
    main()
