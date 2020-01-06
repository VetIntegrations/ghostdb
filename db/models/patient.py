import uuid
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, Date, Text, Numeric, DateTime, JSON
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func

from .. import meta, sqltypes


class Breed(meta.Base):
    __tablename__ = 'breeds'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Breed {}>'.format(self.name)


class Color(meta.Base):
    __tablename__ = 'colors'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Color {}>'.format(self.name)


class Gender(meta.Base):
    __tablename__ = 'genders'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Gender {}>'.format(self.name)


class Species(meta.Base):
    __tablename__ = 'species'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Species {}>'.format(self.name)


class WeightUnit(meta.Base):
    __tablename__ = 'weightunits'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<WeightUnit {}>'.format(self.name)


class Patient(meta.Base):
    __tablename__ = 'patients'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), nullable=False)
    registration_date = Column(Date)
    birthdate = Column(Date)
    breed_id = Column(sqltypes.UUID, ForeignKey('breeds.id'))
    color_id = Column(sqltypes.UUID, ForeignKey('colors.id'))
    gender_id = Column(sqltypes.UUID, ForeignKey('genders.id'))
    species_id = Column(sqltypes.UUID, ForeignKey('species.id'))
    microchip = Column(String(20), unique=True)  # FDXA - 10 digits, FDXB - 15 digits
    microchip_registered = Column(Boolean, default=False)
    neutered = Column(Boolean)
    deceased_date = Column(Date)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    is_deceased = Column(Boolean, default=False)
    is_dnr = Column(Boolean)
    is_mixed = Column(Boolean)
    notes = Column(Text)
    weight = Column(Numeric)
    weight_unit_id = Column(sqltypes.UUID, ForeignKey('weightunits.id'))
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    owners = association_proxy('pet_owners', 'client')
    breed = relationship('Breed')
    color = relationship('Color')
    gender = relationship('Gender')
    species = relationship('Species')
    weight_unit = relationship('WeightUnit')


class Owner(meta.Base):
    __tablename__ = 'owners'

    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'), primary_key=True)
    patient_id = Column(sqltypes.UUID, ForeignKey('patients.id'), primary_key=True)
    is_primary = Column(Boolean)

    client = relationship('Client', backref=backref('client_pets'))
    patient = relationship('Patient', backref=backref('pet_owners'))
