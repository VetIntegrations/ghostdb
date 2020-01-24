from .utils import base
from .pet_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class PetAction:

    create = base.action_factory(create_act.PetCreate, tuple(), tuple())
    update = base.action_factory(update_act.PetUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.PetDelete, tuple(), tuple())


class BreedAction:

    create = base.action_factory(create_act.BreedCreate, tuple(), tuple())
    update = base.action_factory(update_act.BreedUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.BreedDelete, tuple(), tuple())


class ColorAction:

    create = base.action_factory(create_act.ColorCreate, tuple(), tuple())
    update = base.action_factory(update_act.ColorUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.ColorDelete, tuple(), tuple())


class GenderAction:

    create = base.action_factory(create_act.GenderCreate, tuple(), tuple())
    update = base.action_factory(update_act.GenderUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.GenderDelete, tuple(), tuple())


class SpeciesAction:

    create = base.action_factory(create_act.SpeciesCreate, tuple(), tuple())
    update = base.action_factory(update_act.SpeciesUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.SpeciesDelete, tuple(), tuple())


class WeightUnitAction:

    create = base.action_factory(create_act.WeightUnitCreate, tuple(), tuple())
    update = base.action_factory(update_act.WeightUnitUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.WeightUnitDelete, tuple(), tuple())
