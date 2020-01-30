from .utils import base
from .business_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class BusinessAction:

    create = base.action_factory(create_act.BusinessCreate)
    update = base.action_factory(update_act.BusinessUpdate)
    delete = base.action_factory(delete_act.BusinessDelete)

    add_contact = base.action_factory(create_act.ContactCreate)
    update_contact = base.action_factory(update_act.ContactUpdate)
    remove_contact = base.action_factory(delete_act.ContactDelete)
