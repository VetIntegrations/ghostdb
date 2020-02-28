from .utils import base
from .pet_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class PetAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.PetCreate)
    update = base.ActionFactory(update_act.PetUpdate)
    delete = base.ActionFactory(delete_act.PetDelete)

    add_owner = base.ActionFactory(create_act.OwnerCreate)


class BreedAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.BreedCreate)
    update = base.ActionFactory(update_act.BreedUpdate)
    delete = base.ActionFactory(delete_act.BreedDelete)


class ColorAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ColorCreate)
    update = base.ActionFactory(update_act.ColorUpdate)
    delete = base.ActionFactory(delete_act.ColorDelete)


class GenderAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.GenderCreate)
    update = base.ActionFactory(update_act.GenderUpdate)
    delete = base.ActionFactory(delete_act.GenderDelete)


class SpeciesAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.SpeciesCreate)
    update = base.ActionFactory(update_act.SpeciesUpdate)
    delete = base.ActionFactory(delete_act.SpeciesDelete)


class WeightUnitAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.WeightUnitCreate)
    update = base.ActionFactory(update_act.WeightUnitUpdate)
    delete = base.ActionFactory(delete_act.WeightUnitDelete)
