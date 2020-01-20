from .utils.base import action_factory
from .corporation_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class CorporationAction:

    create = action_factory(create_act.Create, tuple(), tuple())
    update = action_factory(update_act.Update, tuple(), tuple())
    delete = action_factory(delete_act.Delete, tuple(), tuple())
