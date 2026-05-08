"""replace cart status enum

Revision ID: 8b2c4e5f1a9c
Revises: f23a56a373af
Create Date: 2026-05-08 00:00:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "8b2c4e5f1a9c"
down_revision = "f23a56a373af"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ux_carts_open_per_customer")
    op.execute("ALTER TABLE carts ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TYPE cart_status RENAME TO cart_status_old")
    op.execute("CREATE TYPE cart_status AS ENUM ('OPEN', 'CHECKOUT', 'PAID')")
    op.execute(
        "ALTER TABLE carts ALTER COLUMN status TYPE cart_status "
        "USING (CASE WHEN status::text = 'CHECKED_OUT' THEN 'CHECKOUT' "
        "ELSE status::text END)::cart_status"
    )
    op.execute("ALTER TABLE carts ALTER COLUMN status SET DEFAULT 'OPEN'")
    op.execute(
        "CREATE UNIQUE INDEX ux_carts_open_per_customer "
        "ON carts (customer_id) WHERE status = 'OPEN'"
    )
    op.execute("DROP TYPE cart_status_old")


def downgrade() -> None:
    pass
