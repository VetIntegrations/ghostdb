import pytest
from datetime import datetime

from ghostdb.db.models.appointment import Appointment
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ghostdb.bl.actions.utils.base import action_factory
from ..update import AppointmentUpdate


class TestAppointmentUpdate:

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
        update_action = action_factory(AppointmentUpdate)

        new_duration = 45
        assert new_duration != self.appointment.duration

        self.appointment.duration = new_duration

        assert default_database.query(Appointment).count() == 1
        appointment, ok = update_action(self.appointment)
        assert ok
        assert appointment == self.appointment
        assert default_database.query(Appointment).count() == 1

        updated_appointment = default_database.query(Appointment)[0]
        assert updated_appointment.id == self.appointment.id
        assert updated_appointment.duration == new_duration

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.appointment import AppointmentAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AppointmentUpdate, 'process', process)

        with pytest.raises(Called):
            AppointmentAction.update(self.appointment)

    def test_update_right_record(self, default_database):
        appointment2 = Appointment(
            business=self.business,
            pet=self.pet,
            scheduled_time=datetime.now(),
            duration=30
        )
        default_database.add(appointment2)

        update_action = action_factory(AppointmentUpdate)

        new_duration = 90
        assert new_duration != self.appointment.duration

        self.appointment.duration = new_duration

        assert default_database.query(Appointment).count() == 2
        _, ok = update_action(self.appointment)
        assert ok
        assert default_database.query(Appointment).count() == 2

        updated_appointment = default_database.query(Appointment).filter(
            Appointment.id == self.appointment.id,
            Appointment.duration == new_duration,
            Appointment.scheduled_time == None,  #noqa  SqlAlchemy doesn't recognize `is`
            Appointment.business == self.business,
            Appointment.pet == self.pet,
        )
        assert updated_appointment.count() == 1

        stay_appointment = default_database.query(Business).filter(
            Appointment.id == appointment2.id,
            Appointment.duration == appointment2.duration,
            Appointment.scheduled_time == appointment2.scheduled_time,
            Appointment.business == self.business,
            Appointment.pet == self.pet,
        )
        assert stay_appointment.count() == 1
