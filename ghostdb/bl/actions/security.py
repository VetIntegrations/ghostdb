from ghostdb.core.event import event
from .utils import base
from .security_actions import create as create_act, delete as delete_act


class TemporaryTokenAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.TemporaryTokenCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    delete = base.ActionFactory(
        delete_act.TemporaryTokenDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )
