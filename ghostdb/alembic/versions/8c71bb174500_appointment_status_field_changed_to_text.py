"""appointment status field changed to text

Revision ID: 8c71bb174500
Revises: ae16495f8747
Create Date: 2020-02-18 08:56:00.508362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c71bb174500'
down_revision = 'ae16495f8747'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'appointments',
        'reason',
        existing_type=sa.Text(),
        nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'appointments',
        'reason',
        existing_type=sa.String(length=500),
        nullable=True
    )
    # ### end Alembic commands ###