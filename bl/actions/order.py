from ghostdb.core.event import event
from .utils import base, validators
from .order_actions import (
    create as create_act, update as update_act, delete as delete_act
)


OrderRequiredFields = validators.RequiredFields(('corporation', 'client', ))


class OrderAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.OrderCreate,
        validators=(OrderRequiredFields, ),
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.OrderUpdate,
        validators=(OrderRequiredFields, ),
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.OrderDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )

    add_item = base.ActionFactory(
        create_act.ItemCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE,
            # TODO [DEV-148]: create data_dumper
        )
    )
    update_item = base.ActionFactory(
        update_act.ItemUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE,
            # TODO [DEV-148]: create data_dumper
        )
    )
    remove_item = base.ActionFactory(
        delete_act.ItemDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE,
            # TODO [DEV-148]: create data_dumper
        )
    )
