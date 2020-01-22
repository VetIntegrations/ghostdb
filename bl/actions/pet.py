from .utils import base
from .pet_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class PetAction:

    create = base.action_factory(create_act.Create, tuple(), tuple())
    update = base.action_factory(update_act.Update, tuple(), tuple())
    delete = base.action_factory(delete_act.Delete, tuple(), tuple())
