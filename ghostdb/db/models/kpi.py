import enum
from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

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


class KPIValue(meta.Base):
    __tablename__ = 'kpi_value'

    id = Column('id', Integer, primary_key=True)

    data_source = Column(Enum(KPIDataSource))
    kind = Column(Enum(KPIKind))
    value = Column(Numeric(16, 2))
    date = Column(Date)

    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=True)
    business_id = Column(sqltypes.UUID, ForeignKey('businesses.id'), nullable=True)
    provider_id = Column(sqltypes.UUID, ForeignKey('providers.id'), nullable=True)
    # location
    # practice_type

    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'), nullable=True)
    pet_id = Column(sqltypes.UUID, ForeignKey('pets.id'), nullable=True)

    revenue_center_id = Column(sqltypes.UUID, ForeignKey('glcode_revenuecenter.id'))
    department_id = Column(sqltypes.UUID, ForeignKey('glcode_department.id'))
    category_id = Column(sqltypes.UUID, ForeignKey('glcode_category.id'))
    class_id = Column(sqltypes.UUID, ForeignKey('glcode_class.id'))
    subclass_id = Column(sqltypes.UUID, ForeignKey('glcode_subclass.id'))
    servicetype_id = Column(sqltypes.UUID, ForeignKey('glcode_servicetype.id'))

    corporation = relationship('Corporation')
    business = relationship('Business')
    provider = relationship('Provider')
    client = relationship('Client')
    pet = relationship('Pet')

    revenue_center = relationship('RevenueCenter')
    department = relationship('Department')
    category = relationship('Category')
    klass = relationship('Class')
    subclass = relationship('SubClass')
    servicetype = relationship('ServiceType')

    def __repr__(self):
        return '<KPI Value {}={} {}>'.format(self.kind, self.value, self.date)
