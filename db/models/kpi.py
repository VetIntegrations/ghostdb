import enum
from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey, Enum

from .. import meta, sqltypes


class KPIKind(enum.Enum):
    FINANCIAL_NET_REVENUE = 'financial_net_revenue'
    FINANCIAL_NET_PROFIT = 'financial_net_profit'


class KPIValue(meta.Base):
    __tablename__ = 'kpi_value'

    pk = Column('id', Integer, primary_key=True)

    kind = Column(Enum(KPIKind))
    value = Column(Numeric)
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

    def __repr__(self):
        return '<KPI Value {}={} {}>'.format(self.kind, self.value, self.date)
