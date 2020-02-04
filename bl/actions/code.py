from .utils import base
from .code_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class RevenueCenterAction:

    create = base.action_factory(create_act.RevenueCenterCreate)
    update = base.action_factory(update_act.RevenueCenterUpdate)
    delete = base.action_factory(delete_act.RevenueCenterDelete)


class DepartmentAction:

    create = base.action_factory(create_act.DepartmentCreate)
    update = base.action_factory(update_act.DepartmentUpdate)
    delete = base.action_factory(delete_act.DepartmentDelete)


class CategoryAction:

    create = base.action_factory(create_act.CategoryCreate)
    update = base.action_factory(update_act.CategoryUpdate)
    delete = base.action_factory(delete_act.CategoryDelete)


class ClassAction:

    create = base.action_factory(create_act.ClassCreate)
    update = base.action_factory(update_act.ClassUpdate)
    delete = base.action_factory(delete_act.ClassDelete)


class SubClassAction:

    create = base.action_factory(create_act.SubClassCreate)
    update = base.action_factory(update_act.SubClassUpdate)
    delete = base.action_factory(delete_act.SubClassDelete)


class ServiceTypeAction:

    create = base.action_factory(create_act.ServiceTypeCreate)
    update = base.action_factory(update_act.ServiceTypeUpdate)
    delete = base.action_factory(delete_act.ServiceTypeDelete)


class ServiceAction:

    create = base.action_factory(create_act.ServiceCreate)
    update = base.action_factory(update_act.ServiceUpdate)
    delete = base.action_factory(delete_act.ServiceDelete)
