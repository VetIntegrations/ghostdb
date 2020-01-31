import typing

from ghostdb.db.models import appointment
from ..utils import base


class AppointmentDelete(base.BaseAction):

    def process(self, _appiontment: appointment.Appointment) -> typing.Tuple[appointment.Appointment, bool]:
        self.db.delete(_appiontment)
        self.db.commit()

        return (_appiontment, True)
