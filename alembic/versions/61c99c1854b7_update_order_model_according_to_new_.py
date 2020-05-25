"""update order model according to new table in VetSuccess

Revision ID: 61c99c1854b7
Revises: 727aa3837572
Create Date: 2020-04-08 16:52:20.259103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61c99c1854b7'
down_revision = '727aa3837572'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('source_type', sa.String(length=50), nullable=True))
    op.add_column('orders', sa.Column('transaction_type', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'transaction_type')
    op.drop_column('orders', 'source_type')
    # ### end Alembic commands ###