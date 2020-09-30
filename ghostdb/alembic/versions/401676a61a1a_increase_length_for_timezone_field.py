"""increase length for timezone field

Revision ID: 401676a61a1a
Revises: 3cb7539c31cb
Create Date: 2020-09-14 10:39:49.549652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '401676a61a1a'
down_revision = '3cb7539c31cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('businesses', 'timezone',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=40),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('businesses', 'timezone',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
    # ### end Alembic commands ###