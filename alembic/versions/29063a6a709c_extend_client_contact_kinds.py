"""extend client contact kinds

Revision ID: 29063a6a709c
Revises: 4f2c90d83a4e
Create Date: 2020-02-21 13:02:08.010219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '29063a6a709c'
down_revision = '4f2c90d83a4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'client_contacts',
        'kind',
        existing_type=mysql.ENUM('MOBILE', 'HOME', 'WORK', 'PHONE', 'FAX', 'SKYPE'),
        nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'client_contacts',
        'kind',
        existing_type=mysql.ENUM('mobile', 'home', 'work', 'skype'),
        nullable=True
    )
    # ### end Alembic commands ###
