from ghostdb.core.event import event
from .utils import base
from .security_actions import create as create_act


class TemporaryTokenAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.TemporaryTokenCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
