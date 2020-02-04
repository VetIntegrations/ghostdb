import uuid
import pytest

from ghostdb.db import meta
from ghostdb.db.models.code import (
    RevenueCenter, Department, Category, Class, SubClass, ServiceType,
    Service, ServiceKind
)


@pytest.mark.parametrize(
    'model, selector_class_name',
    (
        (RevenueCenter, 'RevenueCenterSelector', ),
        (Department, 'DepartmentSelector', ),
        (Category, 'CategorySelector', ),
        (Class, 'ClassSelector', ),
        (SubClass, 'SubClassSelector', ),
        (ServiceType, 'ServiceTypeSelector', ),
    )
)
class TestServiceRelatedModelsByID:

    @pytest.fixture(autouse=True)
    def setup(self, model, selector_class_name, default_database):
        self.obj = model(name='FooBar')
        default_database.add(self.obj)
        default_database.commit()

    def test_ok(self, model, selector_class_name, default_database):
        from .. import code

        obj, ok = getattr(code, selector_class_name).by_id(self.obj.id)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_not_found(self, model, selector_class_name, default_database):
        from .. import code

        obj, ok = getattr(code, selector_class_name).by_id(uuid.uuid4())

        assert not ok
        assert obj is None


@pytest.mark.parametrize(
    'model, selector_class_name',
    (
        (RevenueCenter, 'RevenueCenterSelector', ),
        (Department, 'DepartmentSelector', ),
        (Category, 'CategorySelector', ),
        (Class, 'ClassSelector', ),
        (SubClass, 'SubClassSelector', ),
        (ServiceType, 'ServiceTypeSelector', ),
    )
)
class TestServiceRelatedModelsByName:

    @pytest.fixture(autouse=True)
    def setup(self, model, selector_class_name, default_database):
        self.obj = model(name='FooBar')
        default_database.add(self.obj)
        default_database.commit()

    def test_ok(self, model, selector_class_name, default_database):
        from .. import code

        obj, ok = getattr(code, selector_class_name).by_name(self.obj.name)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_not_found(self, model, selector_class_name, default_database):
        from .. import code

        obj, ok = getattr(code, selector_class_name).by_name('Foo')

        assert not ok
        assert obj is None


class TestServiceByID:

    @pytest.fixture(autouse=True)
    def setup_service(self, default_database):
        self.service = Service(name='FooBar', kind=ServiceKind.service)
        default_database.add(self.service)
        default_database.commit()

    def test_ok(self, default_database):
        from ..code import ServiceSelector

        service, ok = ServiceSelector.by_id(self.service.id)

        assert ok
        assert service.id == self.service.id
        assert service.name == self.service.name
        assert service.kind == self.service.kind

    def test_not_found(self, default_database):
        from ..code import ServiceSelector

        service, ok = ServiceSelector.by_id(uuid.uuid4())

        assert not ok
        assert service is None


class TestServiceByName:

    @pytest.fixture(autouse=True)
    def setup_service(self, default_database):
        self.service = Service(name='FooBar', kind=ServiceKind.service)
        default_database.add(self.service)
        default_database.commit()

    def test_ok(self, default_database):
        from ..code import ServiceSelector

        service, ok = ServiceSelector.by_name(self.service.name)

        assert ok
        assert service.id == self.service.id
        assert service.name == self.service.name
        assert service.kind == self.service.kind

    def test_not_found(self, default_database):
        print('~~~>', default_database, meta.DATABASES)
        from ..code import ServiceSelector

        service, ok = ServiceSelector.by_name('Foo')

        assert not ok
        assert service is None
