import enum
import uuid
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, JSON, Enum, DateTime, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func

from .. import meta
from .. import sqltypes


class Client(meta.Base):
    __tablename__ = 'clients'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    bussiness_name = Column(String(200))
    last_name = Column(String(100))
    first_name = Column(String(100))
    email = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    note = Column(Text)
    pms_ids = Column(JSON)

    # clinic? VetSuccess.practice_id

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    addresses = relationship('ClientAddress', back_populates='client')
    contacts = relationship('ClientContact', back_populates='client')

    pets = association_proxy('client_pets', 'patient')

    def __repr__(self):
        if self.bussiness_name:
            label = 'business name'
            value = self.bussiness_name
        else:
            label = 'name'
            value = ' '.join((self.first_name, self.last_name))

        return '<Client({}={})>'.format(label, value)


class AddressKind(enum.Enum):
    home = 'Home'
    work = 'Work'
    temporary = 'Temporary'


class ClientAddress(meta.Base):
    __tablename__ = 'client_addresses'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'))
    kind = Column(Enum(AddressKind))
    is_primary = Column(Boolean, default=False)
    zip_code = Column(String(20))
    country = Column(String(50))
    city = Column(String(100))
    state = Column(String(50))
    address = Column(String(200))
    note = Column(Text)

    client = relationship('Client', back_populates='addresses')


class ContactKind(enum.Enum):
    mobile = 'Mobile Phone'
    home = 'Home Phone'
    work = 'Work Phone'
    skype = 'Skype'


class ClientContact(meta.Base):
    __tablename__ = 'client_contacts'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'))
    kind = Column(Enum(ContactKind))
    is_primary = Column(Boolean, default=False)
    name = Column(String(50))
    value = Column(String(50))
    note = Column(Text)

    client = relationship('Client', back_populates='contacts')
