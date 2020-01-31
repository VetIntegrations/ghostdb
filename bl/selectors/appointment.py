from ghostdb.db.models import appointment
from .utils import base, generic


class AppointmentSelector:

    by_id = base.selector_factory(generic.ByID, appointment.Appointment)
