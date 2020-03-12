import uuid
import pytest
from collections import namedtuple

from ..bus import BaseEventBus
from ..event import BaseEvent, InternalEvent
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
