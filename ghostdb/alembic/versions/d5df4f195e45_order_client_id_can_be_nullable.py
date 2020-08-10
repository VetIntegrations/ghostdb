"""order.client_id can be nullable

Revision ID: d5df4f195e45
Revises: 475e9af57299
Create Date: 2020-08-07 08:51:54.024613

"""
import ghostdb
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5df4f195e45'
down_revision = '475e9af57299'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('orders', 'client_id', existing_type=sa.BINARY(length=16), nullable=True)


def downgrade():
    op.alter_column('orders', 'client_id', existing_type=sa.BINARY(length=16), nullable=False)
