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

bind = op.get_bind()
metadata = sa.MetaData()


def get_data(file_name: str) -> list[dict[str, Any]]:
    """Return data to insert from initial data CSV file.

    :param file_name: path to the CSV file with data
    :return: list of dicts with data to insert: key - column name, value - value to insert
    """
    file_path = data_dir / file_name
    df = pd.read_csv(file_path, delimiter=";")
    return df.to_dict("records")


def upgrade() -> None:
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
    ]
    for tbl in tables:
        op.execute(f"TRUNCATE TABLE {tbl} CASCADE;")
