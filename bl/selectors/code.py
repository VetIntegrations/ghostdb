from ghostdb.db.models import code
from .utils import base, generic
from .code_selectors import by_name as by_name_selector


class RevenueCenterSelector:

    by_id = base.selector_factory(generic.ByID, code.RevenueCenter)
    by_name = base.selector_factory(by_name_selector.ByName, code.RevenueCenter)


class DepartmentSelector:

    by_id = base.selector_factory(generic.ByID, code.Department)
    by_name = base.selector_factory(by_name_selector.ByName, code.Department)


class CategorySelector:

    by_id = base.selector_factory(generic.ByID, code.Category)
    by_name = base.selector_factory(by_name_selector.ByName, code.Category)


class ClassSelector:

    by_id = base.selector_factory(generic.ByID, code.Class)
    by_name = base.selector_factory(by_name_selector.ByName, code.Class)


class SubClassSelector:

    by_id = base.selector_factory(generic.ByID, code.SubClass)
    by_name = base.selector_factory(by_name_selector.ByName, code.SubClass)


class ServiceTypeSelector:

    by_id = base.selector_factory(generic.ByID, code.ServiceType)
    by_name = base.selector_factory(by_name_selector.ByName, code.ServiceType)


class ServiceSelector:

    by_id = base.selector_factory(generic.ByID, code.Service)
    by_name = base.selector_factory(by_name_selector.ByName, code.Service)
