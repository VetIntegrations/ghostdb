from .utils import base
from .client_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ClientAction:

    create = base.action_factory(create_act.ClientCreate, tuple(), tuple())
    update = base.action_factory(update_act.ClientUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.ClientDelete, tuple(), tuple())

    add_contact = base.action_factory(create_act.ContactCreate, tuple(), tuple())
    update_contact = base.action_factory(update_act.ContactUpdate, tuple(), tuple())
    remove_contact = base.action_factory(delete_act.ContactDelete, tuple(), tuple())

    add_address = base.action_factory(create_act.AddressCreate, tuple(), tuple())
    update_address = base.action_factory(update_act.AddressUpdate, tuple(), tuple())
    remove_address = base.action_factory(delete_act.AddressDelete, tuple(), tuple())
