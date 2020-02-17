from ghostdb.db.models import appointment
from .utils import base, generic


class AppointmentSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, appointment.Appointment)


class AppointmentSourceSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, appointment.AppointmentSource)
    by_iname = base.SelectorFactory(generic.ByIName, appointment.AppointmentSource)


class AppointmentKindSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, appointment.AppointmentKind)
    by_iname = base.SelectorFactory(generic.ByIName, appointment.AppointmentKind)
