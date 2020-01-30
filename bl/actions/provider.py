from .utils import base
from .provider_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ProviderAction:

    create = base.action_factory(create_act.ProviderCreate)
    update = base.action_factory(update_act.ProviderUpdate)
    delete = base.action_factory(delete_act.ProviderDelete)

    add_contact = base.action_factory(create_act.ContactCreate)
    update_contact = base.action_factory(update_act.ContactUpdate)
    remove_contact = base.action_factory(delete_act.ContactDelete)
