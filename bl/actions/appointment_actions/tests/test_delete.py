import pytest
from datetime import datetime

from ghostdb.db.models.appointment import Appointment
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ghostdb.bl.actions.utils.base import action_factory
from ..delete import AppointmentDelete


class TestAppointmentDelete:

    @pytest.fixture(autouse=True)
    def setup_appointment(self, default_database):
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

        default_database.add(self.corp)
        default_database.add(self.business)
        default_database.add(self.pet)
        default_database.add(self.appointment)
        default_database.commit()

    def test_ok(self, default_database):
        delete_action = action_factory(AppointmentDelete)

        assert default_database.query(Appointment).count() == 1
        _, ok = delete_action(self.appointment)
        assert ok
        assert default_database.query(Appointment).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.appointment import AppointmentAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AppointmentDelete, 'process', process)

        with pytest.raises(Called):
            AppointmentAction.delete(self.appointment)

    def test_delete_right_record(self, default_database):
        appointment2 = Appointment(
            business=self.business,
            pet=self.pet,
            scheduled_time=datetime.now(),
            duration=30
        )
        default_database.add(appointment2)

        delete_action = action_factory(AppointmentDelete)

        assert default_database.query(Appointment).count() == 2
        _, ok = delete_action(self.appointment)
        assert ok
        assert default_database.query(Appointment).count() == 1

        assert default_database.query(Appointment)[0] == appointment2
