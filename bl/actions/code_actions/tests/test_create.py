import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ghostdb.bl.actions.code import (
    RevenueCenterAction, DepartmentAction, CategoryAction, ClassAction,
    SubClassAction, ServiceTypeAction, ServiceAction
)
from ..create import (
    RevenueCenterCreate, DepartmentCreate, CategoryCreate, ClassCreate,
    SubClassCreate, ServiceTypeCreate, ServiceCreate
)


@pytest.mark.parametrize(
    'model, action_class, actionset',
    (
        (RevenueCenter, RevenueCenterCreate, RevenueCenterAction, ),
        (Department, DepartmentCreate, DepartmentAction, ),
        (Category, CategoryCreate, CategoryAction, ),
        (Class, ClassCreate, ClassAction, ),
        (SubClass, SubClassCreate, SubClassAction, ),
        (ServiceType, ServiceTypeCreate, ServiceTypeAction, ),
    )
)
class TestCodeRelatedModelsCreate:

    def test_ok(
        self,
        model,
        action_class,
        actionset,
        dbsession,
        event_off
    ):
        obj = model(name='FooBar')

        assert dbsession.query(model).count() == 0
        new_obj, ok = actionset(dbsession).create(obj)
        assert ok
        assert new_obj == obj
        assert dbsession.query(model).filter(model.name == 'FooBar').count() == 1

        event_off.assert_called_once()

    def test_action_class_use_right_action(
        self,
        model,
        action_class,
        actionset,
        dbsession,
        monkeypatch,
        event_off
    ):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(action_class, 'process', process)

        obj = model(name='FooBar')
        with pytest.raises(Called):
            actionset(dbsession).create(obj)


class TestServiceCreate:

    def test_ok(self, dbsession, event_off):
        service = Service(name='FooBar', kind=ServiceKind.PRODUCT)

        assert dbsession.query(Service).count() == 0
        new_service, ok = ServiceAction(dbsession).create(service)
        assert ok
        assert new_service == service
        assert dbsession.query(Service).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ServiceCreate, 'process', process)

        service = Service(name='FooBar', kind=ServiceKind.SERVICE)
        with pytest.raises(Called):
            ServiceAction(dbsession).create(service)
