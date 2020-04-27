from functools import partial

from ghostdb.core.event import event, data_dumper
from .utils import base
from .pet_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class PetAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.PetCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.PetUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.PetDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )

    add_owner = base.ActionFactory(
        create_act.OwnerCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE,
            data_dumper=partial(
                data_dumper.RelationDataDumper,
                pk_fields=("client_id", "pet_id", )
            )
        )
    )


class BreedAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.BreedCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.BreedUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.BreedDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class ColorAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.ColorCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.ColorUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.ColorDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class GenderAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.GenderCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.GenderUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.GenderDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class SpeciesAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.SpeciesCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.SpeciesUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.SpeciesDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )


class WeightUnitAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.WeightUnitCreate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_CREATE
        )
    )
    update = base.ActionFactory(
        update_act.WeightUnitUpdate,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_UPDATE
        )
    )
    delete = base.ActionFactory(
        delete_act.WeightUnitDelete,
        event_factory=base.EventFactory(
            event_name=event.EVENT_RECORD_DELETE
        )
    )
