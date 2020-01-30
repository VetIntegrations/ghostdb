from .utils import base
from .pet_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class PetAction:

    create = base.action_factory(create_act.PetCreate)
    update = base.action_factory(update_act.PetUpdate)
    delete = base.action_factory(delete_act.PetDelete)


class BreedAction:

    create = base.action_factory(create_act.BreedCreate)
    update = base.action_factory(update_act.BreedUpdate)
    delete = base.action_factory(delete_act.BreedDelete)


class ColorAction:

    create = base.action_factory(create_act.ColorCreate)
    update = base.action_factory(update_act.ColorUpdate)
    delete = base.action_factory(delete_act.ColorDelete)


class GenderAction:

    create = base.action_factory(create_act.GenderCreate)
    update = base.action_factory(update_act.GenderUpdate)
    delete = base.action_factory(delete_act.GenderDelete)


class SpeciesAction:

    create = base.action_factory(create_act.SpeciesCreate)
    update = base.action_factory(update_act.SpeciesUpdate)
    delete = base.action_factory(delete_act.SpeciesDelete)


class WeightUnitAction:

    create = base.action_factory(create_act.WeightUnitCreate)
    update = base.action_factory(update_act.WeightUnitUpdate)
    delete = base.action_factory(delete_act.WeightUnitDelete)
