from ghostdb.core.event import event
from .utils import base
from .business_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class BusinessAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.BusinessCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.BusinessUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.BusinessDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )

    add_contact = base.ActionFactory(
        create_act.ContactCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE,
            # TODO [DEV-148]: create data_dumper
        )
    )
    update_contact = base.ActionFactory(
        update_act.ContactUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE,
            # TODO [DEV-148]: create data_dumper
        )
    )
    remove_contact = base.ActionFactory(
        delete_act.ContactDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE,
            # TODO [DEV-148]: create data_dumper
        )
    )
