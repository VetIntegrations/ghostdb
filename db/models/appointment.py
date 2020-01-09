import enum
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

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


class Appointment(meta.Base):
    __tablename__ = 'appointments'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    practice_id = Column(sqltypes.UUID, ForeignKey('practices.id'))
    provider_id = Column(sqltypes.UUID, ForeignKey('providers.id'))
    patient_id = Column(sqltypes.UUID, ForeignKey('patients.id'))
    duration = Column(Integer)
    scheduled_time = Column(DateTime)
    status = Column(Enum(Status))
    reason = Column(String(500))
    note = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    practice = relationship('Practice', backref=backref('appointments'))
    provider = relationship('Provider', backref=backref('appointments'))
    patient = relationship('Patient', backref=backref('appointments'))

    def __repr__(self):
        return '<Appointment patient={} date={}>'.format(self.patient_id, self.scheduled_time)
