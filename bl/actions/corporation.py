from .utils import base
from .corporation_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class CorporationAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.Create)
    update = base.ActionFactory(update_act.Update)
    delete = base.ActionFactory(delete_act.Delete)
