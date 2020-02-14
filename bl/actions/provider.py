from .utils import base
from .provider_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class ProviderAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ProviderCreate)
    update = base.ActionFactory(update_act.ProviderUpdate)
    delete = base.ActionFactory(delete_act.ProviderDelete)

    add_contact = base.ActionFactory(create_act.ContactCreate)
    update_contact = base.ActionFactory(update_act.ContactUpdate)
    remove_contact = base.ActionFactory(delete_act.ContactDelete)


class ProviderKindAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ProviderKindCreate)
    update = base.ActionFactory(update_act.ProviderKindUpdate)
    delete = base.ActionFactory(delete_act.ProviderKindDelete)
