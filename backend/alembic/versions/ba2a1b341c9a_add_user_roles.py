"""add user roles

Revision ID: ba2a1b341c9a
Revises: 8878b7368e97
Create Date: 2026-07-24 22:08:47.086909
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "ba2a1b341c9a"
down_revision: Union[str, Sequence[str], None] = "8878b7368e97"
branch_labels = None
depends_on = None

# Définition de l'ENUM PostgreSQL
user_roles = sa.Enum(
    "admin",
    "advisor",
    "farmer",
    name="user_roles",
)


def upgrade() -> None:
    # Créer le type ENUM
    user_roles.create(op.get_bind(), checkfirst=True)

    # Ajouter la colonne
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_roles,
            nullable=False,
            server_default="farmer",
        ),
    )

    # Supprimer la valeur par défaut pour les nouvelles lignes
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "role")

    # Supprimer le type ENUM
    user_roles.drop(op.get_bind(), checkfirst=True)
