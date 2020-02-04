import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ghostdb.bl.actions.utils.base import action_factory
from ..create import (
    RevenueCenterCreate, DepartmentCreate, CategoryCreate, ClassCreate,
    SubClassCreate, ServiceTypeCreate, ServiceCreate
)


@pytest.mark.parametrize(
    'model, action_class, actionset_name',
    (
        (RevenueCenter, RevenueCenterCreate, 'RevenueCenterAction', ),
        (Department, DepartmentCreate, 'DepartmentAction', ),
        (Category, CategoryCreate, 'CategoryAction', ),
        (Class, ClassCreate, 'ClassAction', ),
        (SubClass, SubClassCreate, 'SubClassAction', ),
        (ServiceType, ServiceTypeCreate, 'ServiceTypeAction', ),
    )
)
class TestCodeRelatedModelsCreate:

    def test_ok(self, model, action_class, actionset_name, default_database):
        create_action = action_factory(action_class)

        obj = model(name='FooBar')

        assert default_database.query(model).count() == 0
        new_obj, ok = create_action(obj)
        assert ok
        assert new_obj == obj
        assert default_database.query(model).filter(model.name == 'FooBar').count() == 1

    def test_action_class_use_right_action(
        self,
        model,
        action_class,
        actionset_name,
        default_database,
        monkeypatch
    ):
        from ghostdb.bl.actions import code

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(action_class, 'process', process)

        obj = model(name='FooBar')
        with pytest.raises(Called):
            getattr(code, actionset_name).create(obj)


class TestServiceCreate:

    def test_ok(self, default_database):
        create_action = action_factory(ServiceCreate)

        service = Service(name='FooBar', kind=ServiceKind.product)

        assert default_database.query(Service).count() == 0
        new_service, ok = create_action(service)
        assert ok
        assert new_service == service
        assert default_database.query(Service).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.code import ServiceAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ServiceCreate, 'process', process)

        service = Service(name='FooBar', kind=ServiceKind.service)
        with pytest.raises(Called):
            ServiceAction.create(service)
