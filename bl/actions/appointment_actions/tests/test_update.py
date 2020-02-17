import pytest
from datetime import datetime

from ghostdb.db.models.appointment import Appointment, AppointmentSource, AppointmentKind
from ghostdb.db.models.business import Business
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.pet import Pet
from ghostdb.bl.actions.appointment import (
    AppointmentAction, AppointmentSourceAction, AppointmentKindAction
)
from ..update import AppointmentUpdate, AppointmentSourceUpdate, AppointmentKindUpdate


class TestAppointmentUpdate:

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
        new_duration = 45
        assert new_duration != self.appointment.duration

        self.appointment.duration = new_duration

        assert dbsession.query(Appointment).count() == 1
        appointment, ok = AppointmentAction(dbsession).update(self.appointment)
        assert ok
        assert appointment == self.appointment
        assert dbsession.query(Appointment).count() == 1

        updated_appointment = dbsession.query(Appointment)[0]
        assert updated_appointment.id == self.appointment.id
        assert updated_appointment.duration == new_duration

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AppointmentUpdate, 'process', process)

        with pytest.raises(Called):
            AppointmentAction(dbsession).update(self.appointment)

    def test_update_right_record(self, dbsession):
        appointment2 = Appointment(
            business=self.business,
            pet=self.pet,
            scheduled_time=datetime.now(),
            duration=30
        )
        dbsession.add(appointment2)

        new_duration = 90
        assert new_duration != self.appointment.duration

        self.appointment.duration = new_duration

        assert dbsession.query(Appointment).count() == 2
        _, ok = AppointmentAction(dbsession).update(self.appointment)
        assert ok
        assert dbsession.query(Appointment).count() == 2

        updated_appointment = dbsession.query(Appointment).filter(
            Appointment.id == self.appointment.id,
            Appointment.duration == new_duration,
            Appointment.scheduled_time == None,  #noqa  SqlAlchemy doesn't recognize `is`
            Appointment.business == self.business,
            Appointment.pet == self.pet,
        )
        assert updated_appointment.count() == 1

        stay_appointment = dbsession.query(Business).filter(
            Appointment.id == appointment2.id,
            Appointment.duration == appointment2.duration,
            Appointment.scheduled_time == appointment2.scheduled_time,
            Appointment.business == self.business,
            Appointment.pet == self.pet,
        )
        assert stay_appointment.count() == 1


@pytest.mark.parametrize(
    'model, action_class, actionset_class',
    (
        (AppointmentSource, AppointmentSourceUpdate, AppointmentSourceAction, ),
        (AppointmentKind, AppointmentKindUpdate, AppointmentKindAction, ),
    )
)
class TestAppointmentRelatedModelsUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, model, action_class, actionset_class, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)

    def test_ok(self, model, action_class, actionset_class, dbsession):
        new_name = 'FooBazz'
        assert new_name != self.obj.name

        self.obj.name = new_name

        assert dbsession.query(model).count() == 1
        obj, ok = actionset_class(dbsession).update(self.obj)
        assert ok
        assert obj == self.obj
        assert dbsession.query(model).count() == 1

        updated_obj = dbsession.query(model)[0]
        assert updated_obj.id == self.obj.id
        assert updated_obj.name == new_name

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
            actionset_class(dbsession).update(self.obj)

    def test_update_right_record(self, model, action_class, actionset_class, dbsession):
        obj = model(name='BarBaz')
        dbsession.add(obj)

        new_name = 'FooBaz'
        assert new_name != self.obj.name

        self.obj.name = new_name

        assert dbsession.query(model).count() == 2
        _, ok = actionset_class(dbsession).update(self.obj)
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
