import typing

from ghostdb.db.models import code
from ..utils import base


class RevenueCenterDelete(base.BaseAction):

    def process(self, revenue_center: code.RevenueCenter) -> typing.Tuple[code.RevenueCenter, bool]:
        self.db.delete(revenue_center)
        self.db.commit()

        return (revenue_center, True)


class DepartmentDelete(base.BaseAction):

    def process(self, department: code.Department) -> typing.Tuple[code.Department, bool]:
        self.db.delete(department)
        self.db.commit()

        return (department, True)


class CategoryDelete(base.BaseAction):

    def process(self, category: code.Category) -> typing.Tuple[code.Category, bool]:
        self.db.delete(category)
        self.db.commit()

        return (category, True)


class ClassDelete(base.BaseAction):

    def process(self, klass: code.Class) -> typing.Tuple[code.Class, bool]:
        self.db.delete(klass)
        self.db.commit()

        return (klass, True)


class SubClassDelete(base.BaseAction):

    def process(self, subclass: code.SubClass) -> typing.Tuple[code.SubClass, bool]:
        self.db.delete(subclass)
        self.db.commit()

        return (subclass, True)


class ServiceTypeDelete(base.BaseAction):

    def process(self, service_type: code.ServiceType) -> typing.Tuple[code.ServiceType, bool]:
        self.db.delete(service_type)
        self.db.commit()

        return (service_type, True)


class ServiceDelete(base.BaseAction):

    def process(self, service: code.Service) -> typing.Tuple[code.Service, bool]:
        self.db.delete(service)
        self.db.commit()

        return (service, True)
