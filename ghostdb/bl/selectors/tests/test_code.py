import uuid
import pytest

from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)
from ..code import (
    RevenueCenterSelector, DepartmentSelector, CategorySelector, ClassSelector,
    SubClassSelector, ServiceTypeSelector, ServiceSelector
)


@pytest.mark.parametrize(
    'model, selector_class',
    (
        (RevenueCenter, RevenueCenterSelector, ),
        (Department, DepartmentSelector, ),
        (Category, CategorySelector, ),
        (Class, ClassSelector, ),
        (SubClass, SubClassSelector, ),
        (ServiceType, ServiceTypeSelector, ),
    )
)
class TestServiceRelatedModelsByID:

    @pytest.fixture(autouse=True)
    def setup(self, model, selector_class, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)
        dbsession.commit()

    def test_ok(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_id(self.obj.id)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_not_found(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert obj is None


@pytest.mark.parametrize(
    'model, selector_class',
    (
        (RevenueCenter, RevenueCenterSelector, ),
        (Department, DepartmentSelector, ),
        (Category, CategorySelector, ),
        (Class, ClassSelector, ),
        (SubClass, SubClassSelector, ),
        (ServiceType, ServiceTypeSelector, ),
    )
)
class TestServiceRelatedModelsByIName:

    @pytest.fixture(autouse=True)
    def setup(self, model, selector_class, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)
        dbsession.commit()

    def test_ok(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_iname(self.obj.name.upper())

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_not_found(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_iname('foo')

        assert not ok
        assert obj is None


class TestServiceByID:

    @pytest.fixture(autouse=True)
    def setup_service(self, dbsession):
        self.service = Service(name='FooBar', kind=ServiceKind.SERVICE)
        dbsession.add(self.service)
        dbsession.commit()

    def test_ok(self, dbsession):
        from ..code import ServiceSelector

        service, ok = ServiceSelector(dbsession).by_id(self.service.id)

        assert ok
        assert service.id == self.service.id
        assert service.name == self.service.name
        assert service.kind == self.service.kind

    def test_not_found(self, dbsession):
        from ..code import ServiceSelector

        service, ok = ServiceSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert service is None


class TestServiceByName:

    @pytest.fixture(autouse=True)
    def setup_service(self, dbsession):
        self.service = Service(name='FooBar', kind=ServiceKind.SERVICE)
        dbsession.add(self.service)
        dbsession.commit()

    def test_ok(self, dbsession):
        service, ok = ServiceSelector(dbsession).by_iname(self.service.name)

        assert ok
        assert service.id == self.service.id
        assert service.name == self.service.name
        assert service.kind == self.service.kind

    def test_not_found(self, dbsession):
        service, ok = ServiceSelector(dbsession).by_iname('Foo')

        assert not ok
        assert service is None
