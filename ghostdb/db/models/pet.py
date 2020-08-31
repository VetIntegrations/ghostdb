import uuid

from sqlalchemy import (
    Column, String, Boolean, ForeignKey, Date, Text, Numeric, DateTime, JSON
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from .. import meta, sqltypes


class Breed(meta.Base):
    __tablename__ = 'breeds'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Breed {}>'.format(self.name)


class Color(meta.Base):
    __tablename__ = 'colors'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Color {}>'.format(self.name)


class Gender(meta.Base):
    __tablename__ = 'genders'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Gender {}>'.format(self.name)


class Species(meta.Base):
    __tablename__ = 'species'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Species {}>'.format(self.name)


class WeightUnit(meta.Base):
    __tablename__ = 'weightunits'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), unique=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<WeightUnit {}>'.format(self.name)


class Pet(meta.Base):
    __tablename__ = 'pets'

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

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    owners = association_proxy('pet_owners', 'client')
    breed = relationship('Breed')
    color = relationship('Color')
    gender = relationship('Gender')
    species = relationship('Species')
    weight_unit = relationship('WeightUnit')

    def __repr__(self):
        return '<Pet name={}>'.format(
            self.name
        )


class PetOwner(meta.Base):
    __tablename__ = 'pet_owners'

    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'), primary_key=True, nullable=False)
    pet_id = Column(sqltypes.UUID, ForeignKey('pets.id'), primary_key=True, nullable=False)
    is_primary = Column(Boolean)

    client = relationship('Client', backref=backref('client_pets'))
    pet = relationship('Pet', backref=backref('pet_owners'))
