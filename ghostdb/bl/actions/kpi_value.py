from ghostdb.core.event import event
from .utils import base
from .kpi_value_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class KPIValueAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.KPIValueCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.KPIValueUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.KPIValueDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )
