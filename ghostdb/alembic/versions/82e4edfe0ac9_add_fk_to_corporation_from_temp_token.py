"""add fk to corporation from temp token

Revision ID: 82e4edfe0ac9
Revises: a65b0fdec7ae
Create Date: 2021-01-18 13:14:41.882146

"""
from alembic import op
import sqlalchemy as sa

import ghostdb


# revision identifiers, used by Alembic.
revision = '82e4edfe0ac9'
down_revision = 'a65b0fdec7ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('temporary_token', sa.Column('corporation_id', ghostdb.db.sqltypes.UUID(), nullable=True))
    op.create_foreign_key(op.f('fk_temporary_token_corporation_id_corporations'), 'temporary_token', 'corporations', ['corporation_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_temporary_token_corporation_id_corporations'), 'temporary_token', type_='foreignkey')
    op.drop_column('temporary_token', 'corporation_id')
    # ### end Alembic commands ###