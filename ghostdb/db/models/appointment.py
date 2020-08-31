import enum
import uuid

from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Text, Integer, Enum, JSON
)
from sqlalchemy.orm import relationship, backref

from .. import meta, sqltypes


class Status(enum.Enum):
    ADMITTED = 'Admitted'
    CANCELLED = 'Cancelled'
    CHECKED_IN = 'Checked In'
    CHECKING_OUT = 'Checking Out'
    COMPLETED = 'Completed'
    CONFIRMED = 'Confirmed'
    DAYCARE = 'Daycare'
    INPROGRESS = 'In Progress'
    MEDBOARD = 'Medboard'
    NOSHOW = 'No Show'
    PENDING = 'Pending'
    PLANNED = 'Planned'
    LATE = 'Late'
    RESERVATION = 'Reservation'
    KEPT = 'Kept'
    RESCHEDULED = 'Rescheduled'
    SCHEDULED = 'Scheduled'


class Appointment(meta.Base):
    __tablename__ = 'appointments'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    business_id = Column(sqltypes.UUID, ForeignKey('businesses.id'), nullable=False)
    provider_id = Column(sqltypes.UUID, ForeignKey('providers.id'))
    pet_id = Column(sqltypes.UUID, ForeignKey('pets.id'), nullable=False)
    source_id = Column(sqltypes.UUID, ForeignKey('appointment_sources.id'))
    kind_id = Column(sqltypes.UUID, ForeignKey('appointment_kinds.id'))
    duration = Column(Integer)
    scheduled_time = Column(DateTime(timezone=True))
    status = Column(Enum(Status))
    reason = Column(Text)
    note = Column(Text)
    pms_ids = Column(JSON, default={})

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    business = relationship('Business', backref=backref('appointments'))
    provider = relationship('Provider', backref=backref('appointments'))
    pet = relationship('Pet', backref=backref('appointments'))
    source = relationship('AppointmentSource', backref=backref('appointments'))
    kind = relationship('AppointmentKind', backref=backref('appointments'))

    def __repr__(self):
        return '<Appointment pet={} date={}>'.format(self.pet_id, self.scheduled_time)


class AppointmentSource(meta.Base):
    __tablename__ = 'appointment_sources'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<AppointmentSource name={}>'.format(self.name)


class AppointmentKind(meta.Base):
    __tablename__ = 'appointment_kinds'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<AppointmentKind name={}>'.format(self.name)
