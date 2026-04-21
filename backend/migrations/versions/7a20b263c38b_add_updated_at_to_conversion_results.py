"""add updated_at to conversion_results

Revision ID: 7a20b263c38b
Revises: 0e34bef6babb
Create Date: 2026-04-21 12:59:00.179946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a20b263c38b"
down_revision = "0e34bef6babb"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("conversion_results", schema=None) as batch_op:
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))

    op.execute(
        """
        UPDATE conversion_results
        SET updated_at = created_at
        WHERE updated_at IS NULL
        """
    )

    with op.batch_alter_table("conversion_results", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False,
        )


def downgrade():
    with op.batch_alter_table("conversion_results", schema=None) as batch_op:
        batch_op.drop_column("updated_at")