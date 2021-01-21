from ghostdb.core.event import event
from .utils import base
from .corporation_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class CorporationAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.Create,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.Update,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    delete = base.ActionFactory(
        delete_act.Delete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )

    add_member = base.ActionFactory(
        create_act.AddMember,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    activate_member = base.ActionFactory(
        update_act.ActivateMember,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    update_member = base.ActionFactory(
        update_act.UpdateMember,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    remove_user_from_members = base.ActionFactory(
        update_act.RemoveUserFromMembers,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete_member = base.ActionFactory(
        delete_act.DeleteMember,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class OrgChartAction(base.BaseActionSet):

    remove_user = base.ActionFactory(
        update_act.OrgChartRemoveUser,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )

    move_member = base.ActionFactory(
        update_act.OrgChartMoveMember,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
