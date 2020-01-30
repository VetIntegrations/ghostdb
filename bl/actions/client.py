from .utils import base
from .client_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ClientAction:

    create = base.action_factory(create_act.ClientCreate)
    update = base.action_factory(update_act.ClientUpdate)
    delete = base.action_factory(delete_act.ClientDelete)

    add_contact = base.action_factory(create_act.ContactCreate)
    update_contact = base.action_factory(update_act.ContactUpdate)
    remove_contact = base.action_factory(delete_act.ContactDelete)

    add_address = base.action_factory(create_act.AddressCreate)
    update_address = base.action_factory(update_act.AddressUpdate)
    remove_address = base.action_factory(delete_act.AddressDelete)
