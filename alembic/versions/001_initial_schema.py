"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-14 13:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create urls table
    op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.Column("short_id", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("short_id"),
    )
    # Create index on short_id for faster lookups
    op.create_index(op.f("ix_urls_short_id"), "urls", ["short_id"], unique=True)


def downgrade() -> None:
    # Drop index
    op.drop_index(op.f("ix_urls_short_id"), table_name="urls")
    # Drop table
    op.drop_table("urls")
