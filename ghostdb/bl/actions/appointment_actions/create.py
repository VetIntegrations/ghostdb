import typing

from ghostdb.db.models import appointment
from ..utils import base


class AppointmentCreate(base.BaseAction):

    def process(self, _appiontment: appointment.Appointment) -> typing.Tuple[appointment.Appointment, bool]:
        self.db.add(_appiontment)
        self.db.commit()

        return (_appiontment, True)


class AppointmentSourceCreate(base.BaseAction):

    def process(self, source: appointment.AppointmentSource) -> typing.Tuple[appointment.AppointmentSource, bool]:
        self.db.add(source)
        self.db.commit()

        return (source, True)


class AppointmentKindCreate(base.BaseAction):

    def process(self, kind: appointment.AppointmentKind) -> typing.Tuple[appointment.AppointmentKind, bool]:
        self.db.add(kind)
        self.db.commit()

        return (kind, True)
