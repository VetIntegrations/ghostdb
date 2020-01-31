import uuid
import pytest

from ghostdb.db.models.appointment import Appointment
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet


class TestByID:

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
        from ..appointment import AppointmentSelector

        appointment, ok = AppointmentSelector.by_id(self.appointment.id)

        assert ok
        assert appointment.id == self.appointment.id
        assert appointment.duration == self.appointment.duration

    def test_not_found(self, default_database):
        from ..appointment import AppointmentSelector

        appointment, ok = AppointmentSelector.by_id(uuid.uuid4())

        assert not ok
        assert appointment is None
