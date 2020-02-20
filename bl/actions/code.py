from .utils import base
from .code_actions import (
    create as create_act, update as update_act, delete as delete_act
)


class RevenueCenterAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.RevenueCenterCreate)
    update = base.ActionFactory(update_act.RevenueCenterUpdate)
    delete = base.ActionFactory(delete_act.RevenueCenterDelete)


class DepartmentAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.DepartmentCreate)
    update = base.ActionFactory(update_act.DepartmentUpdate)
    delete = base.ActionFactory(delete_act.DepartmentDelete)


class CategoryAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.CategoryCreate)
    update = base.ActionFactory(update_act.CategoryUpdate)
    delete = base.ActionFactory(delete_act.CategoryDelete)


class ClassAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ClassCreate)
    update = base.ActionFactory(update_act.ClassUpdate)
    delete = base.ActionFactory(delete_act.ClassDelete)


class SubClassAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.SubClassCreate)
    update = base.ActionFactory(update_act.SubClassUpdate)
    delete = base.ActionFactory(delete_act.SubClassDelete)


class ServiceTypeAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ServiceTypeCreate)
    update = base.ActionFactory(update_act.ServiceTypeUpdate)
    delete = base.ActionFactory(delete_act.ServiceTypeDelete)


class ServiceAction(base.BaseActionSet):

    create = base.ActionFactory(create_act.ServiceCreate)
    update = base.ActionFactory(update_act.ServiceUpdate)
    delete = base.ActionFactory(delete_act.ServiceDelete)
