from .utils import base, validators
from .order_actions import (
    create as create_act, update as update_act, delete as delete_act
)


OrderRequiredFields = validators.RequiredFields(('corporation', 'client', 'pet', 'provider', ))


class OrderAction:

    create = base.action_factory(
        create_act.OrderCreate,
        validators=(OrderRequiredFields, )
    )
    update = base.action_factory(
        update_act.OrderUpdate,
        validators=(OrderRequiredFields, )
    )
    delete = base.action_factory(delete_act.OrderDelete)

    add_item = base.action_factory(create_act.ItemCreate)
    update_item = base.action_factory(update_act.ItemUpdate)
    remove_item = base.action_factory(delete_act.ItemDelete)
