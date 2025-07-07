"""populate_initial_data

Revision ID: 2112c1c93f89
Revises: 8e1456d1a51e
Create Date: 2024-09-28 14:06:55.365543

"""
import os
from pathlib import Path
from typing import Any, Sequence, Union

from alembic import op
import pandas as pd
import sqlalchemy as sa

SCHEMA = os.environ.get('DB_SCHEMA')
data_dir = Path().resolve() / "initial_data"

# revision identifiers, used by Alembic.
revision: str = '2112c1c93f89'
down_revision: Union[str, None] = '8e1456d1a51e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def get_data(file_name: str) -> list[dict[str, Any]]:
    """Return data to insert from initial data CSV file.

    :param file_name: path to the CSV file with data
    :return: list of dicts with data to insert: key - column name, value - value to insert
    """
    file_path = data_dir / file_name
    df = pd.read_csv(file_path, delimiter=";")
    return df.to_dict("records")


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()
    tables = [
        "oas",
        "tolerance_uom",
        "horizontal_acc",
        "vertical_acc",
        "lighting",
        "marking",
        "obstacle_type",
        "verif_status",

    ]
    for tbl_name in tables:
        tbl = sa.Table(tbl_name, metadata, schema=SCHEMA, autoload_with=bind)
        op.bulk_insert(tbl, get_data(f"{tbl_name}.csv"))


    tbl_dof_conf = sa.Table("dof_conf", metadata, schema=SCHEMA, autoload_with=bind)
    op.bulk_insert(
        tbl_dof_conf,
        [
            {
                "file_type": "csv",
                "revision_date": "2019-09-08",
                "settings": {
                  "csv_table_map": {
                    "VERIFIED STATUS": "verif_status_code",
                    "CITY": "city",
                    "QUANTITY": "quantity",
                    "AGL": "agl",
                    "AMSL": "amsl",
                    "LIGHTING": "lighting_code",
                    "MARKING": "marking_code",
                    "FAA STUDY": "faa_study_number",
                    "ACTION": "action",
                    "JDATE": "julian_date"
                  },
                  "coordinates_map": {
                    "LATDEC": "lat",
                    "LONDEC": "lon"
                  },
                  "parsed_map": {
                    "oas_ident": "OAS",
                    "accuracy": "ACCURACY",
                    "obstacle_type": "TYPE"
                  }
                }
            }
        ]
    )


def downgrade() -> None:
    tables = [
        f"{SCHEMA}.oas",
        f"{SCHEMA}.tolerance_uom",
        f"{SCHEMA}.horizontal_acc",
        f"{SCHEMA}.vertical_acc",
        f"{SCHEMA}.lighting",
        f"{SCHEMA}.marking",
        f"{SCHEMA}.obstacle_type",
        f"{SCHEMA}.verif_status"
        f"{SCHEMA}.dof_conf"
    ]
    for tbl in tables:
        op.execute(f"TRUNCATE TABLE {tbl} CASCADE;")
