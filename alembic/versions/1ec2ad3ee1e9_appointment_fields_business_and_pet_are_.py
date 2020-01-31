"""appointment fields business and pet are required

Revision ID: 1ec2ad3ee1e9
Revises: 1245c66dfc76
Create Date: 2020-01-31 10:40:53.272590

"""
from alembic import op
import sqlalchemy as sa

import ghostdb


# revision identifiers, used by Alembic.
revision = '1ec2ad3ee1e9'
down_revision = '1245c66dfc76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments', 'business_id',
               existing_type=sa.BINARY(length=16),
               nullable=False)
    op.alter_column('appointments', 'pet_id',
               existing_type=sa.BINARY(length=16),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments', 'pet_id',
               existing_type=sa.BINARY(length=16),
               nullable=True)
    op.alter_column('appointments', 'business_id',
               existing_type=sa.BINARY(length=16),
               nullable=True)
    # ### end Alembic commands ###
