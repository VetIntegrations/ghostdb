import typing

from ghostdb.db.models import appointment
from ..utils import base


class AppointmentDelete(base.BaseAction):

    def process(self, _appiontment: appointment.Appointment) -> typing.Tuple[appointment.Appointment, bool]:
        self.db.delete(_appiontment)
        self.db.commit()

        return (_appiontment, True)


class AppointmentSourceDelete(base.BaseAction):

    def process(self, source: appointment.AppointmentSource) -> typing.Tuple[appointment.AppointmentSource, bool]:
        self.db.delete(source)
        self.db.commit()

        return (source, True)


class AppointmentKindDelete(base.BaseAction):

    def process(self, kind: appointment.AppointmentKind) -> typing.Tuple[appointment.AppointmentKind, bool]:
        self.db.delete(kind)
        self.db.commit()

        return (kind, True)
