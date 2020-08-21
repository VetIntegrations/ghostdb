import enum
import uuid
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Boolean, JSON, Enum, Text
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from .. import meta, sqltypes


class ProviderKind(meta.Base):
    __tablename__ = 'provider_kinds'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)
    is_doctor = Column(Boolean)

    def __repr__(self):
        return '<ProviderKind {}>'.format(self.name)


class Provider(meta.Base):
    __tablename__ = 'providers'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    business_id = Column(sqltypes.UUID, ForeignKey('businesses.id'))
    kind_id = Column(sqltypes.UUID, ForeignKey('provider_kinds.id'))
    first_name = Column(String(200))
    last_name = Column(String(200))
    is_user = Column(Boolean)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    kind = relationship('ProviderKind', backref=backref('providers'))
    business = relationship('Business', backref=backref('providers'))

    def __repr__(self):
        return '<Provider fist_name={} last_name={}>'.format(
            self.first_name,
            self.last_name
        )

    @property
    def full_name(self):
        return ' '.join(filter(None, (self.first_name, self.last_name)))


class ProviderContactKind(enum.Enum):
    phone = 'Phone'
    email = 'Email'
    website = 'Website'


class ProviderContact(meta.Base):
    __tablename__ = 'provider_contacts'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    provider_id = Column(sqltypes.UUID, ForeignKey('providers.id'))
    kind = Column(Enum(ProviderContactKind))
    is_primary = Column(Boolean, default=False)
    name = Column(String(50))
    value = Column(String(100))
    note = Column(Text)

    provider = relationship('Provider', backref=backref('contacts'))

    def __repr__(self):
        return '<ProviderContact provider_id={} kind={} value={}>'.format(
            self.provider_id,
            self.kind,
            self.value
        )
