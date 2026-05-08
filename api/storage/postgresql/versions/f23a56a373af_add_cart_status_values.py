"""add cart status values

Revision ID: f23a56a373af
Revises: 334fe8266ec4
Create Date: 2026-05-08 00:00:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "f23a56a373af"
down_revision = "334fe8266ec4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE cart_status ADD VALUE IF NOT EXISTS 'CHECKOUT'")
    op.execute("ALTER TYPE cart_status ADD VALUE IF NOT EXISTS 'PAID'")


def downgrade() -> None:
    pass
