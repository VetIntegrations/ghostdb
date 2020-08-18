import enum
import uuid
from sqlalchemy import (
    select,
    Table, Column, String, Boolean, ForeignKey, JSON, Enum, DateTime, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func

from .. import meta
from .. import sqltypes


class FamilyRelation(enum.Enum):
    parent = 'Parent'
    child = 'Child'


Family = Table(
    'client_family',
    meta.Base.metadata,
    Column('id', sqltypes.UUID, default=uuid.uuid4, primary_key=True),
    Column('from_client_id', sqltypes.UUID, ForeignKey('clients.id'), primary_key=True),
    Column('to_client_id', sqltypes.UUID, ForeignKey('clients.id'), primary_key=True),
    Column('relation', Enum(FamilyRelation))
)


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
    pms_ids = Column(JSON, default={})

    # clinic? VetSuccess.practice_id

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    addresses = relationship('ClientAddress', back_populates='client')
    contacts = relationship('ClientContact', back_populates='client')

    pets = association_proxy('client_pets', 'pet')

    def __repr__(self):
        return '<Client fist_name={} last_name={}>'.format(
            self.first_name,
            self.last_name
        )


family_union = (
    select([Family.c.from_client_id, Family.c.to_client_id, ])
    .union(select([Family.c.to_client_id, Family.c.from_client_id, ]))
    .alias()
)


Client.family = relationship(
    "Client",
    secondary=family_union,
    primaryjoin=Client.id == family_union.c.from_client_id,
    secondaryjoin=Client.id == family_union.c.to_client_id,
    viewonly=True
)


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
    pms_ids = Column(JSON, default={})

    client = relationship('Client', back_populates='addresses')


class ClientContactKind(enum.Enum):

    MOBILE = 'Mobile Phone'
    HOME = 'Home Phone'
    WORK = 'Work Phone'
    PHONE = 'Phone'
    FAX = 'Fax'
    SKYPE = 'Skype'


class ClientContact(meta.Base):
    __tablename__ = 'client_contacts'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'))
    kind = Column(Enum(ClientContactKind))
    is_primary = Column(Boolean, default=False)
    name = Column(String(50))
    value = Column(String(50))
    note = Column(Text)
    pms_ids = Column(JSON, default={})

    client = relationship('Client', back_populates='contacts')
