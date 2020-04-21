from functools import partial

from ..base import BaseAction


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
