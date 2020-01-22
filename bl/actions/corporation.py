from .utils import base
from .corporation_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class CorporationAction:

    create = base.action_factory(create_act.Create, tuple(), tuple())
    update = base.action_factory(update_act.Update, tuple(), tuple())
    delete = base.action_factory(delete_act.Delete, tuple(), tuple())
