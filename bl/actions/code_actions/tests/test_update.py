import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ghostdb.bl.actions.code import (
    RevenueCenterAction, DepartmentAction, CategoryAction, ClassAction,
    SubClassAction, ServiceTypeAction, ServiceAction
)
from ..update import (
    RevenueCenterUpdate, DepartmentUpdate, CategoryUpdate, ClassUpdate,
    SubClassUpdate, ServiceTypeUpdate, ServiceUpdate
)


@pytest.mark.parametrize(
    'model, action_class, actionset',
    (
        (RevenueCenter, RevenueCenterUpdate, RevenueCenterAction, ),
        (Department, DepartmentUpdate, DepartmentAction, ),
        (Category, CategoryUpdate, CategoryAction, ),
        (Class, ClassUpdate, ClassAction, ),
        (SubClass, SubClassUpdate, SubClassAction, ),
        (ServiceType, ServiceTypeUpdate, ServiceTypeAction, ),
    )
)
class TestCodeRelatedModelsUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, model, action_class, actionset, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)

    def test_ok(
        self,
        model,
        action_class,
        actionset,
        dbsession,
        event_off
    ):
        new_name = 'FooBazz'
        assert new_name != self.obj.name

        self.obj.name = new_name

        assert dbsession.query(model).count() == 1
        obj, ok = actionset(dbsession).update(self.obj)
        assert ok
        assert obj == self.obj
        assert dbsession.query(model).count() == 1
        event_off.assert_called_once()

        updated_obj = dbsession.query(model)[0]
        assert updated_obj.id == self.obj.id
        assert updated_obj.name == new_name

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
            actionset(dbsession).update(self.obj)

    def test_update_right_record(
        self,
        model,
        action_class,
        actionset,
        dbsession,
        event_off
    ):
        obj = model(name='BarBaz')
        dbsession.add(obj)

        new_name = 'FooBaz'
        assert new_name != self.obj.name

        self.obj.name = new_name

        assert dbsession.query(model).count() == 2
        _, ok = actionset(dbsession).update(self.obj)
        assert ok
        assert dbsession.query(model).count() == 2

        updated_obj = dbsession.query(model).filter(
            model.id == self.obj.id,
            model.name == new_name
        )
        assert updated_obj.count() == 1

        stay_obj = dbsession.query(model).filter(
            model.id == obj.id,
            model.name == obj.name
        )
        assert stay_obj.count() == 1


class TestServiceUpdate:

    @pytest.fixture(autouse=True)
    def setup_service(self, dbsession):
        self.service = Service(name='FooBar', kind=ServiceKind.SERVICE)
        dbsession.add(self.service)

    def test_ok(self, dbsession, event_off):
        new_name = 'BarBuz'
        assert new_name != self.service.name

        self.service.name = new_name

        assert dbsession.query(Service).count() == 1
        service, ok = ServiceAction(dbsession).update(self.service)
        assert ok
        assert service == self.service
        assert dbsession.query(Service).count() == 1
        event_off.assert_called_once()

        updated_service = dbsession.query(Service)[0]
        assert updated_service.id == self.service.id
        assert updated_service.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ServiceUpdate, 'process', process)

        with pytest.raises(Called):
            ServiceAction(dbsession).update(self.service)

    def test_update_right_record(self, dbsession, event_off):
        service = Service(name='FooBaz', kind=ServiceKind.PRODUCT)
        dbsession.add(service)

        new_name = 'BarBuz'
        assert new_name != self.service.name

        self.service.name = new_name

        assert dbsession.query(Service).count() == 2
        _, ok = ServiceAction(dbsession).update(self.service)
        assert ok
        assert dbsession.query(Service).count() == 2

        updated_service = dbsession.query(Service).filter(
            Service.id == self.service.id,
            Service.name == new_name
        )
        assert updated_service.count() == 1

        stay_service = dbsession.query(Service).filter(
            Service.id == service.id,
            Service.name == service.name
        )
        assert stay_service.count() == 1
