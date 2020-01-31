from .utils import base
from .appointment_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class AppointmentAction:

    create = base.action_factory(create_act.AppointmentCreate)
    update = base.action_factory(update_act.AppointmentUpdate)
    delete = base.action_factory(delete_act.AppointmentDelete)
