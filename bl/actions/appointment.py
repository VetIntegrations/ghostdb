from ghostdb.core.event import event
from .utils import base
from .appointment_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class AppointmentAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.AppointmentCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.AppointmentUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.AppointmentDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class AppointmentSourceAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.AppointmentSourceCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.AppointmentSourceUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.AppointmentSourceDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class AppointmentKindAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.AppointmentKindCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.AppointmentKindUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.AppointmentKindDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )
