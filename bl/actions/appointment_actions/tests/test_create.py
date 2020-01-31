import pytest

from ghostdb.db.models.appointment import Appointment
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ghostdb.bl.actions.utils.base import action_factory
from ..create import AppointmentCreate


class TestAppointmentCreate:

    @pytest.fixture(autouse=True)
    def setup(self, default_database):
        self.corp = Corporation(name='Test Corporation 1')
        self.business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        self.pet = Pet(name='Ricky')

        default_database.add(self.corp)
        default_database.add(self.business)
        default_database.add(self.pet)
        default_database.commit()

    def test_ok(self, default_database):
        create_action = action_factory(AppointmentCreate)

        appointment = Appointment(
            business_id=self.business.id,
            pet_id=self.pet.id,
            duration=30
        )

        assert default_database.query(Appointment).count() == 0
        new_appointment, ok = create_action(appointment)
        assert ok
        assert new_appointment == appointment
        assert default_database.query(Appointment).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.appointment import AppointmentAction

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
            AppointmentAction.create(appointment)
