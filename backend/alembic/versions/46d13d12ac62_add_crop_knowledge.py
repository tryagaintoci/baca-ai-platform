"""add crop knowledge

Revision ID: 46d13d12ac62
Revises: 16c8e7634aac
Create Date: 2026-07-29 02:22:45.342110

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "46d13d12ac62"
down_revision: Union[str, Sequence[str], None] = "16c8e7634aac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


growth_stage_enum = sa.Enum(
    "GERMINATION",
    "VEGETATIVE",
    "FLOWERING",
    "FRUITING",
    "MATURITY",
    "HARVEST",
    name="growthstage",
)


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "crop_knowledge",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("common_name", sa.String(length=100), nullable=False),
        sa.Column("scientific_name", sa.String(length=150), nullable=False),
        sa.Column("family", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("optimal_ph_min", sa.Float(), nullable=False),
        sa.Column("optimal_ph_max", sa.Float(), nullable=False),
        sa.Column("min_temperature", sa.Float(), nullable=False),
        sa.Column("max_temperature", sa.Float(), nullable=False),
        sa.Column("water_requirement", sa.String(length=50), nullable=False),
        sa.Column("growth_duration_days", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_crop_knowledge_common_name"),
        "crop_knowledge",
        ["common_name"],
        unique=True,
    )

    # Création du type ENUM PostgreSQL
    growth_stage_enum.create(op.get_bind(), checkfirst=True)

    # Suppression temporaire du DEFAULT
    op.execute("ALTER TABLE crops ALTER COLUMN growth_stage DROP DEFAULT")

    # Conversion VARCHAR -> ENUM
    op.alter_column(
        "crops",
        "growth_stage",
        existing_type=sa.VARCHAR(length=50),
        type_=growth_stage_enum,
        existing_nullable=False,
        postgresql_using="growth_stage::growthstage",
    )

    # Remise du DEFAULT
    op.execute(
        "ALTER TABLE crops "
        "ALTER COLUMN growth_stage "
        "SET DEFAULT 'VEGETATIVE'::growthstage"
    )

    op.create_unique_constraint(
        "uq_weather_field_date",
        "weather",
        ["field_id", "forecast_date"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_weather_field_date",
        "weather",
        type_="unique",
    )

    # Suppression du DEFAULT ENUM
    op.execute("ALTER TABLE crops ALTER COLUMN growth_stage DROP DEFAULT")

    # Conversion ENUM -> VARCHAR
    op.alter_column(
        "crops",
        "growth_stage",
        existing_type=growth_stage_enum,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
        postgresql_using="growth_stage::text",
    )

    # Remise du DEFAULT texte
    op.execute("ALTER TABLE crops ALTER COLUMN growth_stage SET DEFAULT 'VEGETATIVE'")

    growth_stage_enum.drop(op.get_bind(), checkfirst=True)

    op.drop_index(
        op.f("ix_crop_knowledge_common_name"),
        table_name="crop_knowledge",
    )

    op.drop_table("crop_knowledge")
