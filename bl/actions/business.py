from .utils import base
from .business_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class BusinessAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.BusinessCreate)
    update = base.ActionFactory(update_act.BusinessUpdate)
    delete = base.ActionFactory(delete_act.BusinessDelete)

    add_contact = base.ActionFactory(create_act.ContactCreate)
    update_contact = base.ActionFactory(update_act.ContactUpdate)
    remove_contact = base.ActionFactory(delete_act.ContactDelete)
