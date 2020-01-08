import enum
import uuid
from sqlalchemy import (
    Column, String, Date, Numeric, DateTime, ForeignKey, JSON, Enum, Boolean,
    Text
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from .. import meta, sqltypes


class Practice(meta.Base):
    __tablename__ = 'practices'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    consolidator_id = Column(sqltypes.UUID, ForeignKey('consolidators.id'))
    name = Column(String(200))
    display_name = Column(String(200))
    open_date = Column(Date)
    longitude = Column(Numeric)
    latitude = Column(Numeric)
    zip_code = Column(String(20))
    country = Column(String(50))
    city = Column(String(100))
    state = Column(String(50))
    address = Column(String(200))
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    consolidator = relationship('Consolidator', backref=backref('practices'))

    def __repr__(self):
        return '<Practice {}>'.format(self.name)


class ContactKind(enum.Enum):
    phone = 'Phone'
    email = 'Email'
    website = 'Website'


class PracticeContact(meta.Base):
    __tablename__ = 'practice_contacts'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    practice_id = Column(sqltypes.UUID, ForeignKey('practices.id'))
    kind = Column(Enum(ContactKind))
    is_primary = Column(Boolean, default=False)
    name = Column(String(50))
    value = Column(String(100))
    note = Column(Text)

    practice = relationship('Practice', backref=backref('contacts'))
