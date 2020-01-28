from .utils import base
from .provider_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ProviderAction:

    create = base.action_factory(create_act.ProviderCreate, tuple(), tuple())
    update = base.action_factory(update_act.ProviderUpdate, tuple(), tuple())
    delete = base.action_factory(delete_act.ProviderDelete, tuple(), tuple())

    add_contact = base.action_factory(create_act.ContactCreate, tuple(), tuple())
    update_contact = base.action_factory(update_act.ContactUpdate, tuple(), tuple())
    remove_contact = base.action_factory(delete_act.ContactDelete, tuple(), tuple())
