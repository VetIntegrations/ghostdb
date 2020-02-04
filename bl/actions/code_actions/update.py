import typing

from ghostdb.db.models import code
from ..utils import base


class RevenueCenterUpdate(base.BaseAction):

    def process(self, revenue_center: code.RevenueCenter) -> typing.Tuple[code.RevenueCenter, bool]:
        self.db.add(revenue_center)
        self.db.commit()

        return (revenue_center, True)


class DepartmentUpdate(base.BaseAction):

    def process(self, department: code.Department) -> typing.Tuple[code.Department, bool]:
        self.db.add(department)
        self.db.commit()

        return (department, True)


class CategoryUpdate(base.BaseAction):

    def process(self, category: code.Category) -> typing.Tuple[code.Category, bool]:
        self.db.add(category)
        self.db.commit()

        return (category, True)


class ClassUpdate(base.BaseAction):

    def process(self, klass: code.Class) -> typing.Tuple[code.Class, bool]:
        self.db.add(klass)
        self.db.commit()

        return (klass, True)


class SubClassUpdate(base.BaseAction):

    def process(self, subclass: code.SubClass) -> typing.Tuple[code.SubClass, bool]:
        self.db.add(subclass)
        self.db.commit()

        return (subclass, True)


class ServiceTypeUpdate(base.BaseAction):

    def process(self, service_type: code.ServiceType) -> typing.Tuple[code.ServiceType, bool]:
        self.db.add(service_type)
        self.db.commit()

        return (service_type, True)


class ServiceUpdate(base.BaseAction):

    def process(self, service: code.Service) -> typing.Tuple[code.Service, bool]:
        self.db.add(service)
        self.db.commit()

        return (service, True)
