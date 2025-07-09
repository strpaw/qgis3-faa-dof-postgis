"""Load DOF CSV file into obstacle table"""
import logging
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine

from .coordinates import dms_to_dd
from .db_utils import DBUtils

OasCode = str
ObstIdent = str
HorAccCode = int
VertAccCode = str


def get_csv_columns(csv_rules: dict[str, Any]) -> list[str]:
    """Return list of column names to load from CSV file.

    :param csv_rules: rules for mapping CSV input data columns to database table columns.
    :return: columns to be imported from input file
    """
    columns = list(csv_rules["csv_table_map"].keys())
    columns.extend(list(csv_rules["coordinates_map"].keys()))
    columns.extend(list(csv_rules["parsed_map"].values()))
    return columns


def parse_oas(oas: str) -> tuple[OasCode, ObstIdent]:
    """Return OAS code and obstacle ident based on oas value

    :param oas: OAS column value
    :return: oas code, obstacle ident
    """
    oas_code, obst_ident = oas.split("-")
    return oas_code, obst_ident


def parse_accuracy(acc: str) -> tuple[HorAccCode, VertAccCode]:
    """Return horizontal and vertical accuracy codes based on accuracy colum value.

    :param acc: accuracy column value
    :return: horizontal accuracy code, vertical accuracy code
    """
    h_acc = acc[0]
    v_acc = acc[1]
    return int(h_acc), v_acc



def load_data(df: pd.DataFrame,
              db_utils: DBUtils) -> None:
    """Load 'prepared' data into PostgreSQL database..

    :param df: prepared data
    :param db_utils: instance of DBUtils class
    """
    gdf = gpd.GeoDataFrame(
        data=df,
        geometry=gpd.points_from_xy(
            x=df.lon,
            y=df.lat
        ),
        crs="EPSG:4326"
    )
    gdf.drop(columns=["lon", "lat"], inplace=True)
    logging.info("Data preparation complete.")

    engine = create_engine(
        "postgresql+psycopg2://{user}:{password}@{host}:5432/{database}".format(
            user=db_utils._user,
            password=db_utils._password,
            host=db_utils._host,
            database=db_utils._database
        ))

    logging.info("Inserting data into auxiliary table...")
    with engine.connect() as con:
        con.execution_options(isolation_level="AUTOCOMMIT")
        gdf.to_postgis(
            name="import_obstacle",
            schema="dof",
            con=con,
            if_exists="replace",
            index=False,
            chunksize=10000
        )
    logging.info("Loading data into auxiliary table completed.")

def load_csv(
        path: Path,
        db_utils: DBUtils,
        obstacle_type_mapping: dict[str, int]
) -> None:
    """Load DOF CSV file into PostgreSQL database.

    :param path: path to the DOF file
    :param db_utils: instance of DBUtils class
    :param obstacle_type_mapping: mapping between obstacle type map from DOF data and obstacle id in database table
    """
    logging.info("Loading obstacles from CSV file (path: %s) initiated.", path)
    csv_config = db_utils.select(query="select settings\n"
                                       "from dof.dof_conf\n"
                                       "where file_type = 'csv';")[0][0]
    logging.info("Preparing data...")
    df = pd.read_csv(
        path,
        usecols=get_csv_columns(csv_config),
        skipinitialspace=True,
    )
    logging.info("CSV data read, number of rows: %d", len(df))
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    df.rename(
        columns=csv_config["csv_table_map"],
        inplace=True
    )
    df.rename(
        columns=csv_config["coordinates_map"],
        inplace=True
    )

    oas_code_column = csv_config["parsed_map"]["oas_ident"]
    df["oas_code"] = df.apply(lambda row: parse_oas(row[oas_code_column])[0], axis=1)
    df["obst_number"] = df.apply(lambda row: parse_oas(row[oas_code_column])[1], axis=1)
    df.drop(columns=[oas_code_column], inplace=True)

    accuracy_column = csv_config["parsed_map"]["accuracy"]
    accuracy_invalid_mask = df[accuracy_column].str.strip().str.len() != 2
    df_invalid_acc = df[accuracy_invalid_mask]
    if not df_invalid_acc.empty:
        logging.info("Number of rows with invalid accuracy column (2 characters expected): %d",
                     len(df_invalid_acc))
        df_invalid_acc.to_csv("invalid_accuracy.csv", index=False)
        df = df.drop(df[accuracy_invalid_mask].index)
    df["hor_acc_code"] = df.apply(lambda row: parse_accuracy(row[accuracy_column])[0], axis=1)
    df["vert_acc_code"] = df.apply(lambda row: parse_accuracy(row[accuracy_column])[1], axis=1)
    df.drop(columns=[accuracy_column], inplace=True)

    obstacle_type_column = csv_config["parsed_map"]["obstacle_type"]
    df["type_id"] = df.apply(lambda row: obstacle_type_mapping[row[obstacle_type_column]], axis=1)
    df.drop(columns=[obstacle_type_column], inplace=True)

    load_data(df=df,
              db_utils=db_utils)
    logging.info("Number of rows loaded into database: %d",len(df))


def load_dat(
        path: Path,
        db_utils: DBUtils,
        obstacle_type_mapping: dict[str, int]
) -> None:
    """Load DOF DAT file into PostgreSQL database.

    :param path: path to the DOF file
    :param db_utils: instance of DBUtils class
    :param obstacle_type_mapping: mapping between obstacle type map from DOF data and obstacle id in database table
    """
    logging.info("Loading obstacles from DAT file (path: %s) initiated.", path)
    dat_config = db_utils.select(query="select settings\n"
                                       "from dof.dof_conf\n"
                                       "where file_type = 'dat';")[0][0]["fields"]

    dat_config = {
        field_name: (field_extent[0] - 1, field_extent[1])
        for field_name, field_extent
        in dat_config.items()
    }

    logging.info("Preparing data...")
    df = pd.read_fwf(
        path,
        sep="\s+",
        skiprows=4,
        colspecs=list(dat_config.values()),
        names=dat_config.keys(),
        dtype={ "obst_number": str}
    )
    df["lon"] = df.apply(lambda row: dms_to_dd(row["lon_src"], 180), axis=1)
    df["lat"] = df.apply(lambda row: dms_to_dd(row["lat_src"], 90), axis=1)
    df.drop(columns=["lon_src", "lat_src"], inplace=True)

    df["type_id"] = df.apply(lambda row: obstacle_type_mapping[row["obst_type"]], axis=1)
    df.drop(columns=["obst_type"], inplace=True)

    df.to_csv("dof_dat_parsed.csv", index=False)
    load_data(df=df,
              db_utils=db_utils)
