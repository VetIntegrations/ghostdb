import pytest

from ghostdb.db.models.appointment import Appointment, AppointmentSource, AppointmentKind
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ghostdb.bl.actions.appointment import (
    AppointmentAction, AppointmentSourceAction, AppointmentKindAction
)
from ..create import AppointmentCreate, AppointmentSourceCreate, AppointmentKindCreate


class TestAppointmentCreate:

    @pytest.fixture(autouse=True)
    def setup(self, dbsession):
        self.corp = Corporation(name='Test Corporation 1')
        self.business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        self.pet = Pet(name='Ricky')

        dbsession.add(self.corp)
        dbsession.add(self.business)
        dbsession.add(self.pet)
        dbsession.commit()

    def test_ok(self, dbsession):
        appointment = Appointment(
            business_id=self.business.id,
            pet_id=self.pet.id,
            duration=30
        )

        assert dbsession.query(Appointment).count() == 0
        new_appointment, ok = AppointmentAction(dbsession).create(appointment)
        assert ok
        assert new_appointment == appointment
        assert dbsession.query(Appointment).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AppointmentCreate, 'process', process)

        appointment = Appointment(
            business_id=self.business.id,
            pet_id=self.pet.id,
            duration=30
        )
        with pytest.raises(Called):
            AppointmentAction(dbsession).create(appointment)


@pytest.mark.parametrize(
    'model, action_class, actionset_class',
    (
        (AppointmentSource, AppointmentSourceCreate, AppointmentSourceAction, ),
        (AppointmentKind, AppointmentKindCreate, AppointmentKindAction, ),
    )
)
class TestAppointmentRelatedModelsCreate:

    def test_ok(self, model, action_class, actionset_class, dbsession):
        obj = model(name='FooBar')

        assert dbsession.query(model).count() == 0
        new_obj, ok = actionset_class(dbsession).create(obj)
        assert ok
        assert new_obj == obj
        assert dbsession.query(model).filter(model.name == 'FooBar').count() == 1

    def test_action_class_use_right_action(
        self,
        model,
        action_class,
        actionset_class,
        dbsession,
        monkeypatch
    ):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(action_class, 'process', process)

        obj = model(name='FooBar')
        with pytest.raises(Called):
            actionset_class(dbsession).create(obj)
