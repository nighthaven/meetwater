"""add_user_table

Revision ID: 75c75c93dd5a
Revises:
Create Date: 2025-11-14 00:28:20.087805

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "75c75c93dd5a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column(
            "level",
            sa.Enum(
                "AQUAPHOBIC", "BEGINNER", "INTERMEDIATE", "CONFIRMED", name="userlevel"
            ),
            nullable=False,
        ),
        sa.Column("representative", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 18) OR representative IS NOT NULL",
            name="user_representative_if_minor_check",
        ),
        sa.CheckConstraint(
            "EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 5",
            name="user_minimum_age_check",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS userlevel;")
