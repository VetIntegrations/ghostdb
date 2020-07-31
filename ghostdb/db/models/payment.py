import uuid
from sqlalchemy import Column, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship

from .. import meta, sqltypes


class Payment(meta.Base):
    __tablename__ = 'payments'

    id = Column(sqltypes.UUID, default=uuid.uuid1, primary_key=True)
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
