"""create_tables

Revision ID: 8e1456d1a51e
Revises: 
Create Date: 2024-09-26 15:03:12.489417

"""
import os
from typing import Sequence, Union

from alembic import op
from geoalchemy2 import Geography
import sqlalchemy as sa

SCHEMA = os.environ.get('DB_SCHEMA')


# revision identifiers, used by Alembic.
revision: str = '8e1456d1a51e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "oas",
        sa.Column("code", sa.CHAR(2), primary_key=True),
        sa.Column("name", sa.VARCHAR(100), nullable=False),
        schema=SCHEMA
    )

    op.create_table(
        "country",
        sa.Column("oas_code", sa.CHAR(2), primary_key=True),
        sa.Column("boundary", Geography("MultiPolygon", srid=4326), nullable=False),
        sa.ForeignKeyConstraint(["oas_code"], [f"{SCHEMA}.oas.code"]),
        schema=SCHEMA
    )

    op.create_table(
        "us_state",
        sa.Column("oas_code", sa.CHAR(2), primary_key=True),
        sa.Column("boundary", Geography("MultiPolygon", srid=4326), nullable=False),
        sa.ForeignKeyConstraint(["oas_code"], [f"{SCHEMA}.oas.code"]),
        schema=SCHEMA
    )

    op.create_table(
        "tolerance_uom",
        sa.Column("id", sa.SMALLINT, primary_key=True),
        sa.Column("uom", sa.VARCHAR(5), nullable=False),
        schema=SCHEMA
    )

    op.create_table(
        "horizontal_acc",
        sa.Column("code", sa.SMALLINT, primary_key=True),
        sa.Column("tolerance_uom_id", sa.SMALLINT, nullable=False),
        sa.Column("tolerance", sa.NUMERIC(5, 1), nullable=False),
        sa.ForeignKeyConstraint(["tolerance_uom_id"], [f"{SCHEMA}.tolerance_uom.id"]),
        schema=SCHEMA
    )

    op.create_table(
        "vertical_acc",
        sa.Column('code', sa.CHAR(1), primary_key=True),
        sa.Column("tolerance_uom_id", sa.SMALLINT, nullable=False),
        sa.Column("tolerance", sa.NUMERIC(5, 1), nullable=False),
        sa.ForeignKeyConstraint(["tolerance_uom_id"], [f"{SCHEMA}.tolerance_uom.id"]),
        schema=SCHEMA
    )

    op.create_table(
        "lighting",
        sa.Column("code", sa.CHAR(1), primary_key=True),
        sa.Column("description", sa.VARCHAR(35), nullable=False, unique=True),
        schema=SCHEMA
    )

    op.create_table(
        "marking",
        sa.Column("code", sa.CHAR(1), primary_key=True),
        sa.Column("description", sa.VARCHAR(35), nullable=False, unique=True),
        schema=SCHEMA
    )

    op.create_table(
        "obstacle_type",
        sa.Column("id", sa.SMALLINT, primary_key=True, autoincrement=True),
        sa.Column("type", sa.VARCHAR(50), nullable=False, unique=True),
        schema=SCHEMA
    )

    op.create_table(
        "verif_status",
        sa.Column("code", sa.CHAR(1), primary_key=True),
        sa.Column("description", sa.VARCHAR(20), nullable=False, unique=True),
        schema=SCHEMA
    )

    op.create_table(
        "obstacle",
        sa.Column("oas_code", sa.CHAR(2), nullable=False),
        sa.Column("obst_number", sa.CHAR(6), nullable=False),
        sa.Column("verif_status_code", sa.CHAR(1), nullable=False),
        sa.Column("type_id", sa.SMALLINT, nullable=False),
        sa.Column("lighting_code", sa.CHAR(1), nullable=False),
        sa.Column("marking_code", sa.CHAR(1), nullable=False),
        sa.Column("hor_acc_code", sa.SMALLINT, nullable=False),
        sa.Column("vert_acc_code", sa.CHAR(1), nullable=False),
        sa.Column("city", sa.VARCHAR(20), nullable=False),
        sa.Column("quantity", sa.SMALLINT, nullable=True),
        sa.Column("agl", sa.NUMERIC(5, 2), nullable=False),
        sa.Column("amsl", sa.NUMERIC(7, 2), nullable=True),
        sa.Column("faa_study_number", sa.CHAR(14), nullable=True),
        sa.Column("action", sa.CHAR(1), nullable=False),
        sa.Column("julian_date", sa.CHAR(7), nullable=True),
        sa.Column("valid_from", sa.Date, nullable=False),
        sa.Column("valid_to", sa.Date, nullable=True),
        sa.Column("insert_user", sa.CHAR(4), nullable=False, server_default=sa.func.current_user()),
        sa.Column("mod_user", sa.CHAR(4), nullable=True),
        sa.Column("insert_timestamp", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("mod_timestamp", sa.DateTime(timezone=False), nullable=True),
        sa.Column("location", Geography("Point", srid=4326), nullable=False),
        sa.PrimaryKeyConstraint("oas_code", "obst_number"),
        sa.ForeignKeyConstraint(
            ["oas_code"], [f"{SCHEMA}.oas.code"]
        ),
        sa.ForeignKeyConstraint(
            ["verif_status_code"], [f"{SCHEMA}.verif_status.code"]
        ),

        sa.ForeignKeyConstraint(
            ["type_id"], [f"{SCHEMA}.obstacle_type.id"]
        ),
        sa.ForeignKeyConstraint(
            ["lighting_code"], [f"{SCHEMA}.lighting.code"]
        ),
        sa.ForeignKeyConstraint(
            ["marking_code"], [f"{SCHEMA}.marking.code"]
        ),
        sa.ForeignKeyConstraint(
            ["hor_acc_code"], [f"{SCHEMA}.horizontal_acc.code"]
        ),
        sa.ForeignKeyConstraint(
            ["vert_acc_code"], [f"{SCHEMA}.vertical_acc.code"]
        ),
        schema=SCHEMA
    )

    op.create_table(
        "dof_conf",
        sa.Column("file_type", sa.CHAR(3), primary_key=True),
        sa.Column("revision_date", sa.Date, nullable=False),
        sa.Column("settings", sa.JSON, nullable=False),
        schema=SCHEMA
    )


def downgrade() -> None:
    op.drop_table("obstacle", schema=SCHEMA)
    op.drop_table("country", schema=SCHEMA)
    op.drop_table("us_state", schema=SCHEMA)
    op.drop_table("oas", schema=SCHEMA)
    op.drop_table("lighting", schema=SCHEMA)
    op.drop_table("marking", schema=SCHEMA)
    op.drop_table("obstacle_type", schema=SCHEMA)
    op.drop_table("verif_status", schema=SCHEMA)
    op.drop_table("horizontal_acc", schema=SCHEMA)
    op.drop_table("vertical_acc", schema=SCHEMA)
    op.drop_table("tolerance_uom", schema=SCHEMA)
    op.drop_table("dof_conf", schema=SCHEMA)
