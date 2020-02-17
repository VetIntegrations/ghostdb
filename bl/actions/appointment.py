from .utils import base
from .appointment_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class AppointmentAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.AppointmentCreate)
    update = base.ActionFactory(update_act.AppointmentUpdate)
    delete = base.ActionFactory(delete_act.AppointmentDelete)


class AppointmentSourceAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.AppointmentSourceCreate)
    update = base.ActionFactory(update_act.AppointmentSourceUpdate)
    delete = base.ActionFactory(delete_act.AppointmentSourceDelete)


class AppointmentKindAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.AppointmentKindCreate)
    update = base.ActionFactory(update_act.AppointmentKindUpdate)
    delete = base.ActionFactory(delete_act.AppointmentKindDelete)
