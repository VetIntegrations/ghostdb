import typing

from ghostdb.db.models import code
from ..utils import base


class RevenueCenterCreate(base.BaseAction):

    def process(self, revenue_center: code.RevenueCenter) -> typing.Tuple[code.RevenueCenter, bool]:
        self.db.add(revenue_center)
        self.db.commit()

        return (revenue_center, True)


class DepartmentCreate(base.BaseAction):

    def process(self, department: code.Department) -> typing.Tuple[code.Department, bool]:
        self.db.add(department)
        self.db.commit()

        return (department, True)


class CategoryCreate(base.BaseAction):

    def process(self, category: code.Category) -> typing.Tuple[code.Category, bool]:
        self.db.add(category)
        self.db.commit()

        return (category, True)


class ClassCreate(base.BaseAction):

    def process(self, klass: code.Class) -> typing.Tuple[code.Class, bool]:
        self.db.add(klass)
        self.db.commit()

        return (klass, True)


class SubClassCreate(base.BaseAction):

    def process(self, subclass: code.SubClass) -> typing.Tuple[code.SubClass, bool]:
        self.db.add(subclass)
        self.db.commit()

        return (subclass, True)


class ServiceTypeCreate(base.BaseAction):

    def process(self, service_type: code.ServiceType) -> typing.Tuple[code.ServiceType, bool]:
        self.db.add(service_type)
        self.db.commit()

        return (service_type, True)


class ServiceCreate(base.BaseAction):

    def process(self, service: code.Service) -> typing.Tuple[code.Service, bool]:
        self.db.add(service)
        self.db.commit()

        return (service, True)
