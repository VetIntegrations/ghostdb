import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ghostdb.bl.actions.code import (
    RevenueCenterAction, DepartmentAction, CategoryAction, ClassAction,
    SubClassAction, ServiceTypeAction, ServiceAction
)
from ..delete import (
    RevenueCenterDelete, DepartmentDelete, CategoryDelete, ClassDelete,
    SubClassDelete, ServiceTypeDelete, ServiceDelete
)


@pytest.mark.parametrize(
    'model, action_class, actionset',
    (
        (RevenueCenter, RevenueCenterDelete, RevenueCenterAction, ),
        (Department, DepartmentDelete, DepartmentAction, ),
        (Category, CategoryDelete, CategoryAction, ),
        (Class, ClassDelete, ClassAction, ),
        (SubClass, SubClassDelete, SubClassAction, ),
        (ServiceType, ServiceTypeDelete, ServiceTypeAction, ),
    )
)
class TestCodeRelatedModelsDelete:

    @pytest.fixture(autouse=True)
    def setup(self, model, action_class, actionset, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)

    def test_ok(self, model, action_class, actionset, dbsession):
        assert dbsession.query(model).count() == 1
        _, ok = actionset(dbsession).delete(self.obj)
        assert ok
        assert dbsession.query(model).count() == 0

    def test_action_class_use_right_action(
        self,
        model,
        action_class,
        actionset,
        dbsession,
        monkeypatch
    ):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(action_class, 'process', process)

        with pytest.raises(Called):
            actionset(dbsession).delete(self.obj)

    def test_delete_right_record(self, model, action_class, actionset, dbsession):
        obj = model(name='BarBaz')
        dbsession.add(obj)

        assert dbsession.query(model).count() == 2
        _, ok = actionset(dbsession).delete(self.obj)
        assert ok
        assert dbsession.query(model).count() == 1

        assert dbsession.query(model)[0] == obj


class TestServiceDelete:

    @pytest.fixture(autouse=True)
    def setup_service(self, dbsession):
        self.service = Service(name='FooBar', kind=ServiceKind.SERVICE)
        dbsession.add(self.service)

    def test_ok(self, dbsession):
        assert dbsession.query(Service).count() == 1
        _, ok = ServiceAction(dbsession).delete(self.service)
        assert ok
        assert dbsession.query(Service).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        from ghostdb.bl.actions.code import ServiceAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ServiceDelete, 'process', process)

        with pytest.raises(Called):
            ServiceAction(dbsession).delete(self.service)

    def test_delete_right_record(self, dbsession):
        service = Service(name='FooBaz', kind=ServiceKind.PRODUCT)
        dbsession.add(service)

        assert dbsession.query(Service).count() == 2
        _, ok = ServiceAction(dbsession).delete(self.service)
        assert ok
        assert dbsession.query(Service).count() == 1

        assert dbsession.query(Service)[0] == service
