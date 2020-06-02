import uuid
import pytest

from ghostdb.db.models.appointment import Appointment, AppointmentSource, AppointmentKind
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ..appointment import (
    AppointmentSelector, AppointmentSourceSelector, AppointmentKindSelector
)


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_appointment(self, dbsession):
        self.corp = Corporation(name='Test Corporation 1')
        self.business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        self.pet = Pet(name='Ricky')
        self.appointment = Appointment(
            business=self.business,
            pet=self.pet,
            duration=30
        )

        dbsession.add(self.corp)
        dbsession.add(self.business)
        dbsession.add(self.pet)
        dbsession.add(self.appointment)
        dbsession.commit()

    def test_ok(self, dbsession):
        appointment, ok = AppointmentSelector(dbsession).by_id(self.appointment.id)

        assert ok
        assert appointment.id == self.appointment.id
        assert appointment.duration == self.appointment.duration

    def test_not_found(self, dbsession):
        appointment, ok = AppointmentSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert appointment is None


@pytest.mark.parametrize(
    'model, selector_class',
    (
        (AppointmentSource, AppointmentSourceSelector, ),
        (AppointmentKind, AppointmentKindSelector, ),
    )
)
class TestAppointmentRelatedModels:

    @pytest.fixture(autouse=True)
    def setup(self, model, selector_class, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)
        dbsession.commit()

    def test_by_id_ok(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_id(self.obj.id)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_by_id_not_found(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert obj is None

    def test_by_iname_ok(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_iname(self.obj.name)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_by_iname_not_found(self, model, selector_class, dbsession):
        obj, ok = selector_class(dbsession).by_iname('FooBuz')

        assert not ok
        assert obj is None
