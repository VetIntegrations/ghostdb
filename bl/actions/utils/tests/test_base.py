import pytest
from functools import partial

from ghostdb.exceptions import NoDefaultDatabase
from ghostdb.core.event.event import BaseEvent
from ..base import BaseAction, action_factory


class TestActionFactory:

    def test_action_factory(self, mock_default_database):

        class FakeEvent(BaseEvent):
            called = False

            def register(self, customer: str, obj):
                return self.messages.append('registered')

            def trigger(self):
                self.called = True
                return self.messages.append('triggered')

        class Action(BaseAction):
            called = False

            def process(self, obj, *args, **kwargs):
                self.called = True
                return (None, True)

        fake_event = FakeEvent(lambda customer: ..., lambda obj: ...)
        validators = [lambda obj: ...]
        pre_processors = [lambda obj, act: ...]
        post_processors = [lambda obj, act: ..., lambda obj, act: ...]

        action = action_factory(Action, fake_event, validators, pre_processors, post_processors)

        assert not action.called

        assert action._validators == validators
        assert action._pre_processors == pre_processors
        assert action._post_processors == post_processors
        action(None)
        assert fake_event.called
        assert fake_event.messages == ['registered', 'triggered']
        assert action.called

    def test_no_default_db(self):
        class Action(BaseAction):
            called = False

            def process(self, obj, *args, **kwargs):
                self.called = True

        with pytest.raises(NoDefaultDatabase):
            action_factory(Action, [], [])


class TestBaseAction:

    def test_workflow(self):
        log = []
        obj = {'name': 'Test'}
        new_obj = {'name', 'Test 2'}
        customer = 'test_customer'

        class FakeEvent(BaseEvent):
            def register(self, customer: str, obj):
                self.messages.append((customer, obj))

            def trigger(self):
                return log.append(('event trigger', (customer, obj)))

        def validator(obj):
            log.append(('validator', obj))

        class Action(BaseAction):
            EVENT_NAME = 'test.event'

            def process(self, obj):
                log.append(('Action.process', obj))
                return (new_obj, True)

        def coprocessor(name, obj, act):
            log.append((name, obj, act))

        fake_event = FakeEvent(customer, obj)

        action = Action(
            None,
            fake_event,
            (validator, ),
            (partial(coprocessor, 'pre_1'), partial(coprocessor, 'pre_2')),
            (partial(coprocessor, 'post_1'), partial(coprocessor, 'post_2')),
        )

        assert len(log) == 0
        action(obj)
        assert log == [
            ('validator', obj),
            ('pre_1', obj, action),
            ('pre_2', obj, action),
            ('Action.process', obj),
            ('event trigger', (customer, obj)),
            ('post_1', new_obj, action),
            ('post_2', new_obj, action),
        ]

    def test_event_processor(self):
        log = []
        obj = {'name': 'Test'}
        new_obj = {'name', 'Test 2'}
        customer = 'test_customer'
        validators = [lambda obj: ...]
        pre_processors = [lambda obj, act: ...]
        post_processors = [lambda obj, act: ..., lambda obj, act: ...]

        class FakeEvent(BaseEvent):
            def register(self, customer: str, obj):
                self.messages.append((customer, obj))

            def trigger(self):
                return log.append(('event trigger', (customer, obj)))

        fake_event = FakeEvent(customer, obj)

        class ActionTrue(BaseAction):
            def process(self, obj):
                return (new_obj, True)

        true_action = ActionTrue(None, fake_event, validators, pre_processors, post_processors)

        assert len(log) == 0
        true_action(obj)
        assert log == [
            ('event trigger', (customer, obj)),
        ]

        log = []

        class ActionFalse(BaseAction):
            def process(self, obj):
                return (new_obj, False)

        false_action = ActionFalse(None, fake_event, validators, pre_processors, post_processors)

        assert len(log) == 0
        false_action(obj)
        assert len(log) == 0
