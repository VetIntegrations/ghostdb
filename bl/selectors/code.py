from ghostdb.db.models import code
from .utils import base, generic


class RevenueCenterSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.RevenueCenter)
    by_iname = base.SelectorFactory(generic.ByIName, code.RevenueCenter)


class DepartmentSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.Department)
    by_iname = base.SelectorFactory(generic.ByIName, code.Department)


class CategorySelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.Category)
    by_iname = base.SelectorFactory(generic.ByIName, code.Category)


class ClassSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.Class)
    by_iname = base.SelectorFactory(generic.ByIName, code.Class)


class SubClassSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.SubClass)
    by_iname = base.SelectorFactory(generic.ByIName, code.SubClass)


class ServiceTypeSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.ServiceType)
    by_iname = base.SelectorFactory(generic.ByIName, code.ServiceType)


class ServiceSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, code.Service)
    by_iname = base.SelectorFactory(generic.ByIName, code.Service)
