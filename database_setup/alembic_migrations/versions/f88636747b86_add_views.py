"""add views

Revision ID: f88636747b86
Revises: 2112c1c93f89
Create Date: 2024-10-18 23:07:54.939860

"""
import os
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

SCHEMA = os.environ.get('DB_SCHEMA')

# revision identifiers, used by Alembic.
revision: str = 'f88636747b86'
down_revision: Union[str, None] = '2112c1c93f89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Note: do not modify ddl_views.sql
    sql_views_script = Path().resolve() / "sql" / "ddl_views.sql"
    with open(sql_views_script, "r", encoding="utf-8") as f:
        content = f.read()
        op.execute(content)


def downgrade() -> None:
    views = [
        "vw_horizontal_acc",
        "vw_lighting",
        "vw_marking",
        "vw_obstacle",
        "vw_obstacle_type",
        "vw_states_countries",
        "vw_verif_status",
        "vw_vertical_acc"
    ]
    for v in views:
        op.execute(f"DROP VIEW IF EXISTS {SCHEMA}.{v};")
