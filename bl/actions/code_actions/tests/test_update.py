import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ghostdb.bl.actions.utils.base import action_factory
from ..update import (
    RevenueCenterUpdate, DepartmentUpdate, CategoryUpdate, ClassUpdate,
    SubClassUpdate, ServiceTypeUpdate, ServiceUpdate
)


@pytest.mark.parametrize(
    'model, action_class, actionset_name',
    (
        (RevenueCenter, RevenueCenterUpdate, 'RevenueCenterAction', ),
        (Department, DepartmentUpdate, 'DepartmentAction', ),
        (Category, CategoryUpdate, 'CategoryAction', ),
        (Class, ClassUpdate, 'ClassAction', ),
        (SubClass, SubClassUpdate, 'SubClassAction', ),
        (ServiceType, ServiceTypeUpdate, 'ServiceTypeAction', ),
    )
)
class TestCodeRelatedModelsUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, model, action_class, actionset_name, default_database):
        self.obj = model(name='FooBar')
        default_database.add(self.obj)

    def test_ok(self, model, action_class, actionset_name, default_database):
        update_action = action_factory(action_class)

        new_name = 'FooBazz'
        assert new_name != self.obj.name

        self.obj.name = new_name

        assert default_database.query(model).count() == 1
        obj, ok = update_action(self.obj)
        assert ok
        assert obj == self.obj
        assert default_database.query(model).count() == 1

        updated_obj = default_database.query(model)[0]
        assert updated_obj.id == self.obj.id
        assert updated_obj.name == new_name

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
            getattr(code, actionset_name).update(self.obj)

    def test_update_right_record(self, model, action_class, actionset_name, default_database):
        obj = model(name='BarBaz')
        default_database.add(obj)

        update_action = action_factory(action_class)

        new_name = 'FooBaz'
        assert new_name != self.obj.name

        self.obj.name = new_name

        assert default_database.query(model).count() == 2
        _, ok = update_action(self.obj)
        assert ok
        assert default_database.query(model).count() == 2

        updated_obj = default_database.query(model).filter(
            model.id == self.obj.id,
            model.name == new_name
        )
        assert updated_obj.count() == 1

        stay_obj = default_database.query(model).filter(
            model.id == obj.id,
            model.name == obj.name
        )
        assert stay_obj.count() == 1


class TestServiceUpdate:

    @pytest.fixture(autouse=True)
    def setup_service(self, default_database):
        self.service = Service(name='FooBar', kind=ServiceKind.service)
        default_database.add(self.service)

    def test_ok(self, default_database):
        update_action = action_factory(ServiceUpdate)

        new_name = 'BarBuz'
        assert new_name != self.service.name

        self.service.name = new_name

        assert default_database.query(Service).count() == 1
        service, ok = update_action(self.service)
        assert ok
        assert service == self.service
        assert default_database.query(Service).count() == 1

        updated_service = default_database.query(Service)[0]
        assert updated_service.id == self.service.id
        assert updated_service.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.code import ServiceAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ServiceUpdate, 'process', process)

        with pytest.raises(Called):
            ServiceAction.update(self.service)

    def test_update_right_record(self, default_database):
        service = Service(name='FooBaz', kind=ServiceKind.product)
        default_database.add(service)

        update_action = action_factory(ServiceUpdate)

        new_name = 'BarBuz'
        assert new_name != self.service.name

        self.service.name = new_name

        assert default_database.query(Service).count() == 2
        _, ok = update_action(self.service)
        assert ok
        assert default_database.query(Service).count() == 2

        updated_service = default_database.query(Service).filter(
            Service.id == self.service.id,
            Service.name == new_name
        )
        assert updated_service.count() == 1

        stay_service = default_database.query(Service).filter(
            Service.id == service.id,
            Service.name == service.name
        )
        assert stay_service.count() == 1
