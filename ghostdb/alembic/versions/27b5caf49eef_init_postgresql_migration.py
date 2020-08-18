"""init postgresql migration

Revision ID: 27b5caf49eef
Revises: 
Create Date: 2020-08-18 11:11:26.177185

"""
from alembic import op
import sqlalchemy as sa
import ghostdb

# revision identifiers, used by Alembic.
revision = '27b5caf49eef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointment_kinds',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_appointment_kinds')),
    sa.UniqueConstraint('name', name=op.f('uq_appointment_kinds_name'))
    )
    op.create_table('appointment_sources',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_appointment_sources')),
    sa.UniqueConstraint('name', name=op.f('uq_appointment_sources_name'))
    )
    op.create_table('breeds',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_breeds')),
    sa.UniqueConstraint('name', name=op.f('uq_breeds_name'))
    )
    op.create_table('clients',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('bussiness_name', sa.String(length=200), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_clients'))
    )
    op.create_table('colors',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_colors')),
    sa.UniqueConstraint('name', name=op.f('uq_colors_name'))
    )
    op.create_table('corporations',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_corporations')),
    sa.UniqueConstraint('name', name=op.f('uq_corporations_name'))
    )
    op.create_table('genders',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genders')),
    sa.UniqueConstraint('name', name=op.f('uq_genders_name'))
    )
    op.create_table('glcode_category',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_category')),
    sa.UniqueConstraint('name', name=op.f('uq_glcode_category_name'))
    )
    op.create_table('glcode_class',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_class')),
    sa.UniqueConstraint('name', name=op.f('uq_glcode_class_name'))
    )
    op.create_table('glcode_department',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_department')),
    sa.UniqueConstraint('name', name=op.f('uq_glcode_department_name'))
    )
    op.create_table('glcode_revenuecenter',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_revenuecenter')),
    sa.UniqueConstraint('name', name=op.f('uq_glcode_revenuecenter_name'))
    )
    op.create_table('glcode_servicetype',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_servicetype')),
    sa.UniqueConstraint('name', name=op.f('uq_glcode_servicetype_name'))
    )
    op.create_table('glcode_subclass',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_subclass')),
    sa.UniqueConstraint('name', name=op.f('uq_glcode_subclass_name'))
    )
    op.create_table('provider_kinds',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('is_doctor', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_provider_kinds')),
    sa.UniqueConstraint('name', name=op.f('uq_provider_kinds_name'))
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
    op.create_table('businesses',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('corporation_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('display_name', sa.String(length=200), nullable=False),
    sa.Column('open_date', sa.Date(), nullable=True),
    sa.Column('longitude', sa.Numeric(), nullable=True),
    sa.Column('latitude', sa.Numeric(), nullable=True),
    sa.Column('zip_code', sa.String(length=20), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['corporation_id'], ['corporations.id'], name=op.f('fk_businesses_corporation_id_corporations')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_businesses'))
    )
    op.create_table('client_addresses',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('kind', sa.Enum('home', 'work', 'temporary', name='addresskind'), nullable=True),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('zip_code', sa.String(length=20), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_client_addresses_client_id_clients')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_client_addresses'))
    )
    op.create_table('client_contacts',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('kind', sa.Enum('MOBILE', 'HOME', 'WORK', 'PHONE', 'FAX', 'SKYPE', name='clientcontactkind'), nullable=True),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('value', sa.String(length=50), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_client_contacts_client_id_clients')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_client_contacts'))
    )
    op.create_table('client_family',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('from_client_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('to_client_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('relation', sa.Enum('parent', 'child', name='familyrelation'), nullable=True),
    sa.ForeignKeyConstraint(['from_client_id'], ['clients.id'], name=op.f('fk_client_family_from_client_id_clients')),
    sa.ForeignKeyConstraint(['to_client_id'], ['clients.id'], name=op.f('fk_client_family_to_client_id_clients')),
    sa.PrimaryKeyConstraint('id', 'from_client_id', 'to_client_id', name=op.f('pk_client_family'))
    )
    op.create_table('corporation_integrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('corporation_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('module', sa.Enum('vetsuccess', name='integrationmodules'), nullable=False),
    sa.Column('auth_credentials', sa.JSON(), nullable=True),
    sa.Column('is_enable', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['corporation_id'], ['corporations.id'], name=op.f('fk_corporation_integrations_corporation_id_corporations')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_corporation_integrations'))
    )
    op.create_table('pets',
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
    sa.ForeignKeyConstraint(['breed_id'], ['breeds.id'], name=op.f('fk_pets_breed_id_breeds')),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], name=op.f('fk_pets_color_id_colors')),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], name=op.f('fk_pets_gender_id_genders')),
    sa.ForeignKeyConstraint(['species_id'], ['species.id'], name=op.f('fk_pets_species_id_species')),
    sa.ForeignKeyConstraint(['weight_unit_id'], ['weightunits.id'], name=op.f('fk_pets_weight_unit_id_weightunits')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pets')),
    sa.UniqueConstraint('microchip', name=op.f('uq_pets_microchip'))
    )
    op.create_table('business_contacts',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('kind', sa.Enum('phone', 'email', 'website', name='businesscontactkind'), nullable=True),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('value', sa.String(length=100), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_business_contacts_business_id_businesses')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_business_contacts'))
    )
    op.create_table('glcode_service',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('category_description', sa.String(length=200), nullable=True),
    sa.Column('kind', sa.Enum('SERVICE', 'PRODUCT', 'INVENTORY', 'ADMIN', 'GROUPITEM', 'DISCOUNT', 'MEDICAL', 'DIAGNOSTIC', 'SALES_TAX', 'PROBLEM', 'PAYMENT', 'TYPE', name='servicekind'), nullable=True),
    sa.Column('revenue_center_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('department_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('category_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('class_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('is_vis_default', sa.Boolean(), nullable=True),
    sa.Column('base_price', sa.Numeric(), nullable=True),
    sa.Column('dispensing_fee', sa.Numeric(), nullable=True),
    sa.Column('paid_doses', sa.Numeric(), nullable=True),
    sa.Column('free_doses', sa.Numeric(), nullable=True),
    sa.Column('unit_of_measure', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_glcode_service_business_id_businesses')),
    sa.ForeignKeyConstraint(['category_id'], ['glcode_category.id'], name=op.f('fk_glcode_service_category_id_glcode_category')),
    sa.ForeignKeyConstraint(['class_id'], ['glcode_class.id'], name=op.f('fk_glcode_service_class_id_glcode_class')),
    sa.ForeignKeyConstraint(['department_id'], ['glcode_department.id'], name=op.f('fk_glcode_service_department_id_glcode_department')),
    sa.ForeignKeyConstraint(['revenue_center_id'], ['glcode_revenuecenter.id'], name=op.f('fk_glcode_service_revenue_center_id_glcode_revenuecenter')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_glcode_service'))
    )
    op.create_table('pet_owners',
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('pet_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_pet_owners_client_id_clients')),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_pet_owners_pet_id_pets')),
    sa.PrimaryKeyConstraint('client_id', 'pet_id', name=op.f('pk_pet_owners'))
    )
    op.create_table('providers',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('kind_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('first_name', sa.String(length=200), nullable=True),
    sa.Column('last_name', sa.String(length=200), nullable=True),
    sa.Column('is_user', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_providers_business_id_businesses')),
    sa.ForeignKeyConstraint(['kind_id'], ['provider_kinds.id'], name=op.f('fk_providers_kind_id_provider_kinds')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_providers'))
    )
    op.create_table('appointments',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('provider_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('pet_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('source_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('kind_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('scheduled_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ADMITTED', 'CANCELLED', 'CHECKED_IN', 'CHECKING_OUT', 'COMPLETED', 'CONFIRMED', 'DAYCARE', 'INPROGRESS', 'MEDBOARD', 'NOSHOW', 'PENDING', 'PLANNED', 'LATE', 'RESERVATION', 'KEPT', 'RESCHEDULED', 'SCHEDULED', name='status'), nullable=True),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_appointments_business_id_businesses')),
    sa.ForeignKeyConstraint(['kind_id'], ['appointment_kinds.id'], name=op.f('fk_appointments_kind_id_appointment_kinds')),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_appointments_pet_id_pets')),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk_appointments_provider_id_providers')),
    sa.ForeignKeyConstraint(['source_id'], ['appointment_sources.id'], name=op.f('fk_appointments_source_id_appointment_sources')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_appointments'))
    )
    op.create_table('glcode_srv_servicetype_rel',
    sa.Column('service_type', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('service', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['service'], ['glcode_service.id'], name=op.f('fk_glcode_srv_servicetype_rel_service_glcode_service')),
    sa.ForeignKeyConstraint(['service_type'], ['glcode_servicetype.id'], name=op.f('fk_glcode_srv_servicetype_rel_service_type_glcode_servicetype'))
    )
    op.create_table('glcode_srv_subclass_rel',
    sa.Column('subclass', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('service', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['service'], ['glcode_service.id'], name=op.f('fk_glcode_srv_subclass_rel_service_glcode_service')),
    sa.ForeignKeyConstraint(['subclass'], ['glcode_subclass.id'], name=op.f('fk_glcode_srv_subclass_rel_subclass_glcode_subclass'))
    )
    op.create_table('kpi_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_source', sa.Enum('PIMS', 'ERP', name='kpidatasource'), nullable=True),
    sa.Column('kind', sa.Enum('FINANCIAL_NET_REVENUE', 'FINANCIAL_NET_PROFIT', 'FINANCIAL_ACCOUNTS_RECEIVABLE', 'FINANCIAL_ACCOUNT_PAYABLE', 'FINANCIAL_COGS', 'FINANCIAL_EBITDA', 'FINANCIAL_CAPEX', 'FINANCIAL_OPEX', name='kpikind'), nullable=True),
    sa.Column('value', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('corporation_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('provider_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('pet_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('revenue_center_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('department_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('category_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('class_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('subclass_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('servicetype_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_kpi_value_business_id_businesses')),
    sa.ForeignKeyConstraint(['category_id'], ['glcode_category.id'], name=op.f('fk_kpi_value_category_id_glcode_category')),
    sa.ForeignKeyConstraint(['class_id'], ['glcode_class.id'], name=op.f('fk_kpi_value_class_id_glcode_class')),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_kpi_value_client_id_clients')),
    sa.ForeignKeyConstraint(['corporation_id'], ['corporations.id'], name=op.f('fk_kpi_value_corporation_id_corporations')),
    sa.ForeignKeyConstraint(['department_id'], ['glcode_department.id'], name=op.f('fk_kpi_value_department_id_glcode_department')),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_kpi_value_pet_id_pets')),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk_kpi_value_provider_id_providers')),
    sa.ForeignKeyConstraint(['revenue_center_id'], ['glcode_revenuecenter.id'], name=op.f('fk_kpi_value_revenue_center_id_glcode_revenuecenter')),
    sa.ForeignKeyConstraint(['servicetype_id'], ['glcode_servicetype.id'], name=op.f('fk_kpi_value_servicetype_id_glcode_servicetype')),
    sa.ForeignKeyConstraint(['subclass_id'], ['glcode_subclass.id'], name=op.f('fk_kpi_value_subclass_id_glcode_subclass')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_kpi_value'))
    )
    op.create_table('orders',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('corporation_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('pet_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('provider_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('invoice_date', sa.DateTime(), nullable=True),
    sa.Column('is_posted', sa.Boolean(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('COLLECTIONS', 'DELETED', 'DUE', 'OPEN', 'PAID', 'UNCOLLECTIBLE', 'VOID', 'CLOSED', 'UNFINISHED', name='orderstatus'), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('site_id', sa.String(length=50), nullable=True),
    sa.Column('transaction_type', sa.String(length=100), nullable=True),
    sa.Column('source_type', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_orders_business_id_businesses')),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_orders_client_id_clients')),
    sa.ForeignKeyConstraint(['corporation_id'], ['corporations.id'], name=op.f('fk_orders_corporation_id_corporations')),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_orders_pet_id_pets')),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk_orders_provider_id_providers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_orders'))
    )
    op.create_table('payments',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('corporation_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('business_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('provider_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('client_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('pet_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('value', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], name=op.f('fk_payments_business_id_businesses')),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('fk_payments_client_id_clients')),
    sa.ForeignKeyConstraint(['corporation_id'], ['corporations.id'], name=op.f('fk_payments_corporation_id_corporations')),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_payments_pet_id_pets')),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk_payments_provider_id_providers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_payments'))
    )
    op.create_table('provider_contacts',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('provider_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('kind', sa.Enum('phone', 'email', 'website', name='providercontactkind'), nullable=True),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], name=op.f('fk_provider_contacts_provider_id_providers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_provider_contacts'))
    )
    op.create_table('order_items',
    sa.Column('id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('order_id', ghostdb.db.sqltypes.UUID(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('service_id', ghostdb.db.sqltypes.UUID(), nullable=True),
    sa.Column('quantity', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('unit_price', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('amount', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('discount_amount', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('paid_doses', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('free_doses', sa.Numeric(precision=16, scale=2), nullable=True),
    sa.Column('is_hidden_on_invoice', sa.Boolean(), nullable=True),
    sa.Column('is_posted', sa.Boolean(), nullable=True),
    sa.Column('is_voided', sa.Boolean(), nullable=True),
    sa.Column('is_depletion_only', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_inventory', sa.Boolean(), nullable=True),
    sa.Column('is_refund', sa.Boolean(), nullable=True),
    sa.Column('pms_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name=op.f('fk_order_items_order_id_orders')),
    sa.ForeignKeyConstraint(['service_id'], ['glcode_service.id'], name=op.f('fk_order_items_service_id_glcode_service')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_order_items'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('provider_contacts')
    op.drop_table('payments')
    op.drop_table('orders')
    op.drop_table('kpi_value')
    op.drop_table('glcode_srv_subclass_rel')
    op.drop_table('glcode_srv_servicetype_rel')
    op.drop_table('appointments')
    op.drop_table('providers')
    op.drop_table('pet_owners')
    op.drop_table('glcode_service')
    op.drop_table('business_contacts')
    op.drop_table('pets')
    op.drop_table('corporation_integrations')
    op.drop_table('client_family')
    op.drop_table('client_contacts')
    op.drop_table('client_addresses')
    op.drop_table('businesses')
    op.drop_table('weightunits')
    op.drop_table('species')
    op.drop_table('provider_kinds')
    op.drop_table('glcode_subclass')
    op.drop_table('glcode_servicetype')
    op.drop_table('glcode_revenuecenter')
    op.drop_table('glcode_department')
    op.drop_table('glcode_class')
    op.drop_table('glcode_category')
    op.drop_table('genders')
    op.drop_table('corporations')
    op.drop_table('colors')
    op.drop_table('clients')
    op.drop_table('breeds')
    op.drop_table('appointment_sources')
    op.drop_table('appointment_kinds')
    # ### end Alembic commands ###
