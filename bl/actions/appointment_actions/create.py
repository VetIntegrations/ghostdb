import typing

from ghostdb.db.models import appointment
from ..utils import base


class AppointmentCreate(base.BaseAction):

    def process(self, _appiontment: appointment.Appointment) -> typing.Tuple[appointment.Appointment, bool]:
        self.db.add(_appiontment)
        self.db.commit()

        return (_appiontment, True)
