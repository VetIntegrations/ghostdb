"""patient models

Revision ID: b2a242bf2bc0
Revises: e1f103c99b27
Create Date: 2020-01-06 14:54:09.474899

"""
from alembic import op
import sqlalchemy as sa

import ghostdb


# revision identifiers, used by Alembic.
revision = 'b2a242bf2bc0'
down_revision = 'e1f103c99b27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('breeds',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_breeds')),
    sa.UniqueConstraint('name', name=op.f('uq_breeds_name'))
    )
    op.create_table('colors',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_colors')),
    sa.UniqueConstraint('name', name=op.f('uq_colors_name'))
    )
    op.create_table('genders',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genders')),
    sa.UniqueConstraint('name', name=op.f('uq_genders_name'))
    )
    op.create_table('species',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_species')),
    sa.UniqueConstraint('name', name=op.f('uq_species_name'))
    )
    op.create_table('weightunits',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_weightunits')),
    sa.UniqueConstraint('name', name=op.f('uq_weightunits_name'))
    )
    op.create_table('patients',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('registration_date', sa.Date(), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('breed_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('color_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('gender_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('species_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('microchip', sa.String(length=20), nullable=True),
    sa.Column('microchip_registered', sa.Boolean(), nullable=True),
    sa.Column('neutered', sa.Boolean(), nullable=True),
    sa.Column('deceased_date', sa.Date(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('is_deceased', sa.Boolean(), nullable=True),
    sa.Column('is_dnr', sa.Boolean(), nullable=True),
    sa.Column('is_mixed', sa.Boolean(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('weight', sa.Numeric(), nullable=True),
    sa.Column('weight_unit_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['breed_id'], ['breeds.id'], name=op.f('fk_patients_breed_id_breeds')),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], name=op.f('fk_patients_color_id_colors')),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], name=op.f('fk_patients_gender_id_genders')),
    sa.ForeignKeyConstraint(['species_id'], ['species.id'], name=op.f('fk_patients_species_id_species')),
    sa.ForeignKeyConstraint(['weight_unit_id'], ['weightunits.id'], name=op.f('fk_patients_weight_unit_id_weightunits')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_patients')),
    sa.UniqueConstraint('microchip', name=op.f('uq_patients_microchip'))
    )
    op.create_table('owners',
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('patient_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_owners_client_id_clients')),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name=op.f('fk_owners_patient_id_patients')),
    sa.PrimaryKeyConstraint('client_id', 'patient_id', name=op.f('pk_owners'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('owners')
    op.drop_table('patients')
    op.drop_table('weightunits')
    op.drop_table('species')
    op.drop_table('genders')
    op.drop_table('colors')
    op.drop_table('breeds')
    # ### end Alembic commands ###
