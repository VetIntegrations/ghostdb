"""extend token kind

Revision ID: 6f21aa205eaa
Revises: 008aeed38f44
Create Date: 2020-11-25 17:15:07.602523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f21aa205eaa'
down_revision = '008aeed38f44'
branch_labels = None
depends_on = None


old_options = ('EMAIL_VALIDATION', 'CORPORATION_INVITE')
new_options = old_options + ('ACCOUNT_DELETION', 'PASSWORD_RECOVERY')

old_type = sa.Enum(*old_options, name='tokenkind')
new_type = sa.Enum(*new_options, name='tokenkind')
tmp_type = sa.Enum(*new_options, name='_tokenkind')

tmp_col = sa.sql.table('temporary_token', sa.Column('kind', new_type, nullable=False))


def upgrade():

    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        'ALTER TABLE temporary_token ALTER COLUMN kind TYPE _tokenkind'
        ' USING kind::text::_tokenkind'
    )
    old_type.drop(op.get_bind(), checkfirst=False)

    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        'ALTER TABLE temporary_token ALTER COLUMN kind TYPE tokenkind'
        ' USING kind::text::tokenkind'
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    pass
