import pytest
from functools import partial

from ghostdb.exceptions import NoDefaultDatabase
from ..base import BaseAction, action_factory


class TestActionFactory:

    def test_action_factory(self, mock_default_database):
        class Action(BaseAction):
            called = False

            def process(self, obj, *args, **kwargs):
                self.called = True
                return (None, True)

        validators = [lambda obj: ...]
        pre_processors = [lambda obj, act: ...]
        post_processors = [lambda obj, act: ..., lambda obj, act: ...]

        action = action_factory(Action, validators, pre_processors, post_processors)

        assert not action.called
        assert action._validators == validators
        assert action._pre_processors == pre_processors
        assert action._post_processors == post_processors
        action(None)
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

        def validator(obj):
            log.append(('validator', obj))

        class Action(BaseAction):
            EVENT_NAME = 'test.event'

            def process(self, obj):
                log.append(('Action.process', obj))
                return (new_obj, True)

        def coprocessor(name, obj, act):
            log.append((name, obj, act))

        action = Action(
            None,
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
            ('post_1', new_obj, action),
            ('post_2', new_obj, action),
        ]
