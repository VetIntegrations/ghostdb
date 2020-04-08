from ghostdb.core.event import event, data_dumper
from .utils import base
from .client_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ClientRelatedDataDumper(data_dumper.GenericDataDumper):

    def get_data_dump(self) -> dict:
        data = super().get_data_dump()
        data['client_id'] = self.obj.client_id.hex

        return data


class ClientAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.ClientCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.ClientUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.ClientDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )

    add_contact = base.ActionFactory(
        create_act.ContactCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE,
            data_dumper=ClientRelatedDataDumper
        )
    )
    update_contact = base.ActionFactory(
        update_act.ContactUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE,
            data_dumper=ClientRelatedDataDumper
        )
    )
    remove_contact = base.ActionFactory(
        delete_act.ContactDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE,
            data_dumper=ClientRelatedDataDumper
        )
    )

    add_address = base.ActionFactory(
        create_act.AddressCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE,
            data_dumper=ClientRelatedDataDumper
        )
    )
    update_address = base.ActionFactory(
        update_act.AddressUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE,
            data_dumper=ClientRelatedDataDumper
        )
    )
    remove_address = base.ActionFactory(
        delete_act.AddressDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE,
            data_dumper=ClientRelatedDataDumper
        )
    )
