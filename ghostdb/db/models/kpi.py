import enum

from sqlalchemy import Column, Integer, Numeric, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .. import meta, sqltypes


class KPIKind(enum.Enum):
    FINANCIAL_NET_REVENUE = 'financial_net_revenue'
    FINANCIAL_NET_PROFIT = 'financial_net_profit'
    FINANCIAL_ACCOUNTS_RECEIVABLE = 'financial_ar'
    FINANCIAL_ACCOUNT_PAYABLE = 'financial_ap'
    FINANCIAL_COGS = 'financial_cogs'
    FINANCIAL_EBITDA = 'financial_ebitda'
    FINANCIAL_CAPEX = 'financial_capex'
    FINANCIAL_OPEX = 'financial_opex'


class KPIDataSource(enum.Enum):
    PIMS = 'pims'
    ERP = 'erp'


class AbstactKPIValue:
    id = Column('id', Integer, primary_key=True)

    data_source = Column(Enum(KPIDataSource))
    kind = Column(Enum(KPIKind))
    value = Column(Numeric(16, 2))
    date = Column(Date)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    @declared_attr
    def corporation_id(self):
        return Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=True)

    @declared_attr
    def business_id(self):
        return Column(sqltypes.UUID, ForeignKey('businesses.id'), nullable=True)

    @declared_attr
    def provider_id(self):
        return Column(sqltypes.UUID, ForeignKey('providers.id'), nullable=True)
    # location
    # practice_type

    @declared_attr
    def client_id(self):
        return Column(sqltypes.UUID, ForeignKey('clients.id'), nullable=True)

    @declared_attr
    def pet_id(self):
        return Column(sqltypes.UUID, ForeignKey('pets.id'), nullable=True)

    @declared_attr
    def revenue_center_id(self):
        return Column(sqltypes.UUID, ForeignKey('glcode_revenuecenter.id'))

    @declared_attr
    def department_id(self):
        return Column(sqltypes.UUID, ForeignKey('glcode_department.id'))

    @declared_attr
    def category_id(self):
        return Column(sqltypes.UUID, ForeignKey('glcode_category.id'))

    @declared_attr
    def class_id(self):
        return Column(sqltypes.UUID, ForeignKey('glcode_class.id'))

    @declared_attr
    def subclass_id(self):
        return Column(sqltypes.UUID, ForeignKey('glcode_subclass.id'))

    @declared_attr
    def servicetype_id(self):
        return Column(sqltypes.UUID, ForeignKey('glcode_servicetype.id'))

    @declared_attr
    def corporation(self):
        return relationship('Corporation')

    @declared_attr
    def business(self):
        return relationship('Business')

    @declared_attr
    def provider(self):
        return relationship('Provider')

    @declared_attr
    def client(self):
        return relationship('Client')

    @declared_attr
    def pet(self):
        return relationship('Pet')

    @declared_attr
    def revenue_center(self):
        return relationship('RevenueCenter')

    @declared_attr
    def department(self):
        return relationship('Department')

    @declared_attr
    def category(self):
        return relationship('Category')

    @declared_attr
    def klass(self):
        return relationship('Class')

    @declared_attr
    def subclass(self):
        return relationship('SubClass')

    @declared_attr
    def servicetype(self):
        return relationship('ServiceType')


class InternalKPIValue(AbstactKPIValue, meta.Base):
    __tablename__ = 'kpi_value_internal'

    def __repr__(self):
        return '<KPI Value {}={} {}>'.format(self.kind, self.value, self.date)


class ExternalKPIValue(AbstactKPIValue, meta.Base):
    __tablename__ = 'kpi_value_external'

    def __repr__(self):
        return '<KPI Value {}={} {}>'.format(self.kind, self.value, self.date)
