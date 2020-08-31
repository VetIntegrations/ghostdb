import enum
import uuid

from sqlalchemy import (
    Column, String, Date, Numeric, DateTime, ForeignKey, JSON, Enum, Boolean,
    Text
)
from sqlalchemy.orm import relationship, backref

from .. import meta, sqltypes


class Business(meta.Base):
    __tablename__ = 'businesses'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=False)
    name = Column(String(200), nullable=False)
    display_name = Column(String(200), nullable=False)
    open_date = Column(Date)
    longitude = Column(Numeric)
    latitude = Column(Numeric)
    timezone = Column(String(20))  # pytz compatible value
    zip_code = Column(String(20))
    country = Column(String(50))
    city = Column(String(100))
    state = Column(String(50))
    address = Column(String(200))
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    corporation = relationship('Corporation', backref=backref('businesses'))

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class BusinessContactKind(enum.Enum):
    phone = 'Phone'
    email = 'Email'
    website = 'Website'


class BusinessContact(meta.Base):
    __tablename__ = 'business_contacts'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    business_id = Column(sqltypes.UUID, ForeignKey('businesses.id'), nullable=False)
    kind = Column(Enum(BusinessContactKind))
    is_primary = Column(Boolean, default=False)
    name = Column(String(50))
    value = Column(String(100), nullable=False)
    note = Column(Text)
    pms_ids = Column(JSON)

    business = relationship('Business', backref=backref('contacts'))

    def __repr__(self):
        return '<BusinessContact business_id={} kind={} value={}>'.format(
            self.practice_id,
            self.kind,
            self.value
        )
