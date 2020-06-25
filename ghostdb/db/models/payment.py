from .. import meta, sqltypes
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship


class Payment(meta.Base):
    __tablename__ = 'payments'

    id = Column('id', Integer, primary_key=True)
    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=True)
    business_id = Column(sqltypes.UUID, ForeignKey('businesses.id'), nullable=True)
    provider_id = Column(sqltypes.UUID, ForeignKey('providers.id'), nullable=True)
    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'), nullable=True)
    pet_id = Column(sqltypes.UUID, ForeignKey('pets.id'), nullable=True)

    value = Column(Numeric(16, 2))
    date = Column(Date)

    corporation = relationship('Corporation')
    business = relationship('Business')
    provider = relationship('Provider')
