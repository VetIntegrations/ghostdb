from functools import partial

from ghostdb.core.event import event, data_dumper
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
            data_dumper=partial(
                data_dumper.RelationDataDumper,
                pk_fields=("order_id", )
            )
        )
    )
    update_item = base.ActionFactory(
        update_act.ItemUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE,
            data_dumper=partial(
                data_dumper.RelationDataDumper,
                pk_fields=("order_id",)
            )
        )
    )
    remove_item = base.ActionFactory(
        delete_act.ItemDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE,
            data_dumper=partial(
                data_dumper.RelationDataDumper,
                pk_fields=("order_id",)
            )
        )
    )
