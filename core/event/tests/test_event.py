import uuid
import pytest
from collections import namedtuple

from ghostdb.bl.actions.utils.base import BaseAction
from ghostdb.bl.actions import (
    appointment, business, client,
    code, order, pet, provider,
)

from ..bus import BaseEventBus
from ..event import (
    BaseEvent, InternalEvent,
    EVENT_RECORD_CREATE,
    EVENT_RECORD_UPDATE,
    EVENT_RECORD_DELETE,
)
from ..exceptions import MissingEventBusException


class TestBaseEvent:

    class FakeEvent(BaseEvent):

        def register(self, customer: str, obj):
            self.messages.append((customer, obj))

    def test_set_event_bus(self):
        class FakeEventBus(BaseEventBus):

            def publish(self, *args):
                ...

        event_bus = FakeEventBus()

        event = self.FakeEvent('test.1', lambda obj: obj)
        assert event.event_bus is None
        event.set_event_bus(event_bus)
        assert event.event_bus == event_bus

    def test_trigger_fails_if_no_event_bus(self):
        event = self.FakeEvent('test.1', lambda obj: obj)

        with pytest.raises(MissingEventBusException):
            event.trigger()

    def test_trigger_send_registered_events(self):
        log = []

        class FakeEventBus(BaseEventBus):

            def publish(self, *args):
                log.append(('publish', *args))

        event_bus = FakeEventBus()

        event = self.FakeEvent('test.1', lambda obj: obj)
        event.set_event_bus(event_bus)

        event.register('test-customer', {'name': 'foo'})
        event.register('test-customer', {'name': 'bar'})

        event.trigger()

        assert log == [
            ('publish', ('test-customer', {'name': 'foo'})),
            ('publish', ('test-customer', {'name': 'bar'})),
        ]

    def test_work_as_context_manager(self):
        log = []

        class FakeEventBus(BaseEventBus):

            def publish(self, *args):
                log.append(('publish', *args))

        event_bus = FakeEventBus()

        with self.FakeEvent('test.1', lambda obj: obj) as event:
            event.set_event_bus(event_bus)

            event.register('test-customer', {'name': 'foo'})
            event.register('test-customer', {'name': 'bar'})

        assert log == [
            ('publish', ('test-customer', {'name': 'foo'})),
            ('publish', ('test-customer', {'name': 'bar'})),
        ]


class TestInternalEvent:

    def test_register(self):
        DataObj = namedtuple('DataObj', 'id, name')

        def fake_data_dumper(obj):
            return {'id': obj.id, 'name': obj.name}

        event = InternalEvent('test.2', fake_data_dumper)

        assert len(event.messages) == 0

        obj = DataObj(uuid.uuid4(), 'foo')
        event.register('test-customer', obj)
        assert len(event.messages) == 1
        assert event.messages[0].format() == {
            'customer': 'test-customer',
            'meta': {
                'event_name': 'test.2',
                'obj': {
                    'model': 'ghostdb.core.event.tests.test_event.DataObj',
                    'pk': obj.id,
                },
            },
            'data': {'id': obj.id, 'name': obj.name},
        }


class TestEvents:

    client_related_action_names = (
        'add_contact',
        'update_contact',
        'remove_contact',
        'add_address',
        'update_address',
        'remove_address',
    )

    pet_related_action_names = (
        'add_owner',
    )

    order_related_action_names = (
        'add_item',
        'update_item',
        'remove_item',
    )

    @pytest.mark.parametrize(
        'actionset_class',
        (
            appointment.AppointmentAction,
            appointment.AppointmentSourceAction,
            appointment.AppointmentKindAction,
            business.BusinessAction,
            client.ClientAction,
            code.RevenueCenterAction,
            code.DepartmentAction,
            code.CategoryAction,
            code.ClassAction,
            code.SubClassAction,
            code.ServiceTypeAction,
            code.ServiceAction,
            order.OrderAction,
            pet.PetAction,
            pet.BreedAction,
            pet.ColorAction,
            pet.GenderAction,
            pet.SpeciesAction,
            pet.WeightUnitAction,
            provider.ProviderAction,
            provider.ProviderKindAction,
        )
    )
    def test_event_name(self, actionset_class):
        actionset = actionset_class(None, None)

        # filter magic methods
        methods_name = [method_name for method_name in dir(actionset) if method_name[:2] != '__']

        for method_name in methods_name:
            action = getattr(actionset, method_name)
            if isinstance(action, BaseAction) and isinstance(action._event, BaseEvent):
                action_name = action.__class__.__name__
                event_name = action._event.name
                if 'Create' in action_name:
                    assert event_name == EVENT_RECORD_CREATE
                elif 'Update' in action_name:
                    assert event_name == EVENT_RECORD_UPDATE
                elif 'Delete' in action_name:
                    assert event_name == EVENT_RECORD_DELETE
                else:
                    assert False, f'{action} must have Create, Update or Delete in the name'

    @pytest.mark.parametrize(
        'actionset_class, action_names, relatited_pk_fields',
        (
            (client.ClientAction, client_related_action_names, ("client_id", )),
            (pet.PetAction, pet_related_action_names, ("client_id", "pet_id", )),
            (order.OrderAction, order_related_action_names, ("order_id", )),
        ),
    )
    def test_event_data_dumper(self, actionset_class, action_names, relatited_pk_fields):
        actionset = actionset_class(None, None)
        for action_name in action_names:
            action = getattr(actionset, action_name)
            data_dumper = action._event.data_dumper(None)
            assert data_dumper.pk_fields == relatited_pk_fields
