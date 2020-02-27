from .utils import base, validators
from .order_actions import (
    create as create_act, update as update_act, delete as delete_act
)


OrderRequiredFields = validators.RequiredFields(('corporation', 'client', ))


class OrderAction(base.BaseActionSet):

    create = base.ActionFactory(
        create_act.OrderCreate,
        validators=(OrderRequiredFields, )
    )
    update = base.ActionFactory(
        update_act.OrderUpdate,
        validators=(OrderRequiredFields, )
    )
    delete = base.ActionFactory(delete_act.OrderDelete)

    add_item = base.ActionFactory(create_act.ItemCreate)
    update_item = base.ActionFactory(update_act.ItemUpdate)
    remove_item = base.ActionFactory(delete_act.ItemDelete)
