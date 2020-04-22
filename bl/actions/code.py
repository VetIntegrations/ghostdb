from ghostdb.core.event import event
from .utils import base
from .code_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class RevenueCenterAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.RevenueCenterCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.RevenueCenterUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.RevenueCenterDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class DepartmentAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.DepartmentCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.DepartmentUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.DepartmentDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class CategoryAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.CategoryCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.CategoryUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.CategoryDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class ClassAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.ClassCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.ClassUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.ClassDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class SubClassAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.SubClassCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.SubClassUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.SubClassDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class ServiceTypeAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.ServiceTypeCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.ServiceTypeUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.ServiceTypeDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class ServiceAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.ServiceCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.ServiceUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.ServiceDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )
