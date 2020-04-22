import pytest
from datetime import datetime

from ghostdb.db.models.appointment import Appointment, AppointmentSource, AppointmentKind
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ghostdb.bl.actions.appointment import (
    AppointmentAction, AppointmentSourceAction, AppointmentKindAction
)
from ..delete import AppointmentDelete, AppointmentSourceDelete, AppointmentKindDelete


class TestAppointmentDelete:

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

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Appointment).count() == 1
        _, ok = AppointmentAction(dbsession).delete(self.appointment)
        assert ok
        assert dbsession.query(Appointment).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AppointmentDelete, 'process', process)

        with pytest.raises(Called):
            AppointmentAction(dbsession).delete(self.appointment)

    def test_delete_right_record(self, dbsession, event_off):
        appointment2 = Appointment(
            business=self.business,
            pet=self.pet,
            scheduled_time=datetime.now(),
            duration=30
        )
        dbsession.add(appointment2)

        assert dbsession.query(Appointment).count() == 2
        _, ok = AppointmentAction(dbsession).delete(self.appointment)
        assert ok
        assert dbsession.query(Appointment).count() == 1

        assert dbsession.query(Appointment)[0] == appointment2


@pytest.mark.parametrize(
    'model, action_class, actionset_class',
    (
        (AppointmentSource, AppointmentSourceDelete, AppointmentSourceAction, ),
        (AppointmentKind, AppointmentKindDelete, AppointmentKindAction, ),
    )
)
class TestAppointmentRelatedModelsDelete:

    @pytest.fixture(autouse=True)
    def setup(self, model, action_class, actionset_class, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)

    def test_ok(
        self,
        model,
        action_class,
        actionset_class,
        dbsession,
        event_off
    ):
        assert dbsession.query(model).count() == 1
        _, ok = actionset_class(dbsession).delete(self.obj)
        assert ok
        assert dbsession.query(model).count() == 0

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

        with pytest.raises(Called):
            actionset_class(dbsession).delete(self.obj)

    def test_delete_right_record(
        self,
        model,
        action_class,
        actionset_class,
        dbsession,
        event_off
    ):
        obj = model(name='BarBaz')
        dbsession.add(obj)

        assert dbsession.query(model).count() == 2
        _, ok = actionset_class(dbsession).delete(self.obj)
        assert ok
        assert dbsession.query(model).count() == 1

        assert dbsession.query(model)[0] == obj
