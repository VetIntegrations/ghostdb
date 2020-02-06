from .utils import base
from .client_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ClientAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ClientCreate)
    update = base.ActionFactory(update_act.ClientUpdate)
    delete = base.ActionFactory(delete_act.ClientDelete)

    add_contact = base.ActionFactory(create_act.ContactCreate)
    update_contact = base.ActionFactory(update_act.ContactUpdate)
    remove_contact = base.ActionFactory(delete_act.ContactDelete)

    add_address = base.ActionFactory(create_act.AddressCreate)
    update_address = base.ActionFactory(update_act.AddressUpdate)
    remove_address = base.ActionFactory(delete_act.AddressDelete)
