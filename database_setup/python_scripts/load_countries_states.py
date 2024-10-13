"""Script to load countries and USA states spatial data into database"""
import argparse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Union

from dacite import from_dict
import geopandas as gpd
from sqlalchemy import create_engine, text
from yaml import safe_load

SrcValue = str  # Country, USA state code/name in the source data file
TargetValue = str  # OAS code in the target database (as in FAA DOF data)


@dataclass(frozen=True)
class DBCredentials:
    """Keep credentials for database"""
    host: str
    database: str
    user: str
    password: str


@dataclass(frozen=True)
class DBSettings:
    """Keep database settings (credentials and others that are should not be hardcoded)"""
    credentials: DBCredentials
    schema: str


@dataclass(frozen=True)
class DataSetConfiguration:
    """Keep settings for data set (country of us states)"""
    src_column: str
    columns_map: dict[SrcValue, TargetValue]


@dataclass(frozen=True)
class Configuration:
    """Keep script configuration"""
    db_settings: DBSettings
    countries: DataSetConfiguration
    us_states: DataSetConfiguration


def load_config(cfg: Union[str, Path] = "load_countries_states_config.yml") -> Configuration:
    """Return configuration.

    :param cfg: path to the configuration file
    :return: instance of script configuration
    """
    with open(cfg, mode="r", encoding="utf-8") as f:
        content = safe_load(f)
        return from_dict(data_class=Configuration,
                         data=content)


def select_features(
        data_path: Union[str, Path],
        src_column: str,
        feat_names: list[str]
) -> gpd.GeoDataFrame:
    """Return country/USA states data (geometry, attributes) - only for countries that are used in DOF

    :param data_path: path to the source file with country data
    :param src_column: column name in source data wth names/codes of countries to load
    :param feat_names: name/codes of countries/USA states to load into database
    :return: data to be inserted into database
    """
    gdf = gpd.read_file(
        data_path,
        columns=[src_column]
    )
    return gdf.loc[gdf[src_column].isin(feat_names)]


def prepare_data(
        data: gpd.GeoDataFrame,
        src_column: str,
        columns_map: dict[SrcValue, TargetValue]
) -> gpd.GeoDataFrame:
    """Return data ready for insert to db: oas_code (identifier used in FAA dof) + geometry

    :param data: raw source data
    :param src_column: column name in source data wth names/codes of countries to load
    :param columns_map: rule between country/USA state name/ident in the source file and oas code
    :return: data with mapped source country/USA states name/ident to oas code
    """
    data["oas_code"] = data[src_column].apply(lambda row: columns_map[row])
    data.drop(columns=[src_column], inplace=True)
    data.rename(columns={"geometry": "boundary"}, inplace=True)
    data.set_geometry("boundary", inplace=True)
    return data


def insert_data(
        data: gpd.GeoDataFrame,
        target_table: str,
        db_settings: DBSettings
) -> None:
    """Insert data into database.

    :param data: data to be loaded
    :param target_table: table name to load data into
    :param db_settings: target database settings (schema, credentials)
    """
    # Some geometries fetched from source data might be a Polygon type, ensure all are MultiPolygons (ST_Multi)
    query_copy = f"""insert into {db_settings.schema}.{target_table} (oas_code, boundary)
                select
                    oas_code,
                    ST_Multi(boundary)::geography
                from dof.{target_table}_tmp;"""
    query_drop = f"drop table if exists dof.{target_table}_tmp;"

    engine = create_engine(
        "postgresql+psycopg2://{user}:{password}@{host}:5432/{database}".format(**asdict(db_settings.credentials)))
    with engine.connect() as con:
        con.execution_options(isolation_level="AUTOCOMMIT")
        data.to_postgis(
            name=f"{target_table}_tmp",
            con=con,
            if_exists="append",
            schema=db_settings.schema,
            index=False,
        )
        con.execute(text(query_copy))
        con.execute(text(query_drop))


def parse_args() -> argparse.Namespace:
    """Parse script arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--settings",
        type=str,
        required=False,
        default="load_countries_states_config.yml",
        help="Path to the configuration file, default: load_countries_states_config.yml"
    )
    parser.add_argument(
        "-c",
        "--countries",
        type=str,
        required=False,
        default="countries.gpkg",
        help="Path to the data file with countries, default: countries.gpkg"
    )
    parser.add_argument(
        "-u",
        "--usa-states",
        type=str,
        required=False,
        default="usa_states.gpkg",
        help="Path to the data file with USA states, default: usa_states.gpkg"
    )
    return parser.parse_args()


def main():
    """Main script loop"""
    args = parse_args()
    config = load_config(args.settings)

    countries = select_features(
        data_path=args.countries,
        src_column=config.countries.src_column,
        feat_names=list(config.countries.columns_map.keys())
    )
    countries = prepare_data(
        data=countries,
        src_column=config.countries.src_column,
        columns_map=config.countries.columns_map
    )
    insert_data(
        data=countries,
        target_table="country",
        db_settings=config.db_settings
    )

    usa_states = select_features(
        data_path=args.usa_states,
        src_column=config.us_states.src_column,
        feat_names=list(config.us_states.columns_map.keys())
    )
    usa_states = prepare_data(
        data=usa_states,
        src_column=config.us_states.src_column,
        columns_map=config.us_states.columns_map
    )
    insert_data(
        data=usa_states,
        target_table="us_state",
        db_settings=config.db_settings
    )


if __name__ == "__main__":
    main()
