import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ghostdb.bl.actions.utils.base import action_factory
from ..delete import (
    RevenueCenterDelete, DepartmentDelete, CategoryDelete, ClassDelete,
    SubClassDelete, ServiceTypeDelete, ServiceDelete
)


@pytest.mark.parametrize(
    'model, action_class, actionset_name',
    (
        (RevenueCenter, RevenueCenterDelete, 'RevenueCenterAction', ),
        (Department, DepartmentDelete, 'DepartmentAction', ),
        (Category, CategoryDelete, 'CategoryAction', ),
        (Class, ClassDelete, 'ClassAction', ),
        (SubClass, SubClassDelete, 'SubClassAction', ),
        (ServiceType, ServiceTypeDelete, 'ServiceTypeAction', ),
    )
)
class TestCodeRelatedModelsDelete:

    @pytest.fixture(autouse=True)
    def setup(self, model, action_class, actionset_name, default_database):
        self.obj = model(name='FooBar')
        default_database.add(self.obj)

    def test_ok(self, model, action_class, actionset_name, default_database):
        delete_action = action_factory(action_class)

        assert default_database.query(model).count() == 1
        _, ok = delete_action(self.obj)
        assert ok
        assert default_database.query(model).count() == 0

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

        with pytest.raises(Called):
            getattr(code, actionset_name).delete(self.obj)

    def test_delete_right_record(self, model, action_class, actionset_name, default_database):
        obj = model(name='BarBaz')
        default_database.add(obj)

        delete_action = action_factory(action_class)

        assert default_database.query(model).count() == 2
        _, ok = delete_action(self.obj)
        assert ok
        assert default_database.query(model).count() == 1

        assert default_database.query(model)[0] == obj


class TestServiceDelete:

    @pytest.fixture(autouse=True)
    def setup_service(self, default_database):
        self.service = Service(name='FooBar', kind=ServiceKind.service)
        default_database.add(self.service)

    def test_ok(self, default_database):
        delete_action = action_factory(ServiceDelete)

        assert default_database.query(Service).count() == 1
        _, ok = delete_action(self.service)
        assert ok
        assert default_database.query(Service).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.code import ServiceAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ServiceDelete, 'process', process)

        with pytest.raises(Called):
            ServiceAction.delete(self.service)

    def test_delete_right_record(self, default_database):
        service = Service(name='FooBaz', kind=ServiceKind.product)
        default_database.add(service)

        delete_action = action_factory(ServiceDelete)

        assert default_database.query(Service).count() == 2
        _, ok = delete_action(self.service)
        assert ok
        assert default_database.query(Service).count() == 1

        assert default_database.query(Service)[0] == service
