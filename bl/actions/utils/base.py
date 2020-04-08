import abc
import typing
import warnings
from collections import OrderedDict
from sqlalchemy.orm import session

from ghostdb.db import meta
from ghostdb import exceptions
from ghostdb.core.event import event, bus


CoProcessor = typing.Callable[[typing.Any, 'BaseAction'], bool]


class BaseActionSet:

    def __init__(self, db: session.Session, event_bus: bus.BaseEventBus = None):
        self.db = db
        self.event_bus = event_bus


class BaseAction(abc.ABC):

    def __init__(
        self,
        db: session.Session,
        event: event.BaseEvent,
        validators: typing.Tuple[typing.Callable],
        pre_processors: typing.Tuple[CoProcessor],
        post_processors: typing.Tuple[CoProcessor]
    ):
        self.db = db
        self._event = event
        self._validators = validators
        self._pre_processors = pre_processors
        self._post_processors = post_processors

    def validate(self, obj: typing.Any) -> bool:
        for validator in self._validators:
            validator(obj)

        return True

    def __call__(self, obj: typing.Any, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        self.validate(obj)

        ret = OrderedDict()
        for processor in self._pre_processors:
            ret[processor] = processor(obj, self)

        if self._event:  # TODO DEV-146, delete this line
            self._event.register('NetSuite', obj)

        obj, ret['process'] = self.process(obj, *args, **kwargs)

        if ret['process']:
            if self._event:  # TODO DEV-146, delete this line
                self._event.trigger()

        for processor in self._post_processors:
            ret[processor] = processor(obj, self)

        return (obj, all(ret.values()))

    @abc.abstractmethod
    def process(self, obj: typing.Any, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        ...


class EventFactory:

    def __init__(self, event_class: event.BaseEvent, event_name: str, data_dumper: typing.Callable):
        self.event_class = event_class
        self.event_name = event_name
        self.data_dumper = data_dumper

    def __call__(self):
        return self.event_class(self.event_name, self.data_dumper)


class ActionFactory:

    def __init__(
        self,
        action_class: BaseAction,
        event_factory: EventFactory = None,  # TODO DEV-146, delete None
        validators: typing.Tuple[typing.Callable] = None,
        pre_processors: typing.Tuple[CoProcessor] = None,
        post_processors: typing.Tuple[CoProcessor] = None
    ):
        self.action_class = action_class
        self.event_factory = event_factory
        self.validators = validators or tuple()
        self.pre_processors = pre_processors or tuple()
        self.post_processors = post_processors or tuple()

    def __get__(self, actionset, _type):
        assert issubclass(_type, BaseActionSet)

        event = self.event_factory()
        event.set_event_bus(actionset.event_bus)

        return self.action_class(
            actionset.db,
            event,
            self.validators,
            self.pre_processors,
            self.post_processors
        )


def action_factory(
    action_class: BaseAction,
    event_processor=None,  # TODO DEV-146, delete None
    validators: typing.Tuple[typing.Callable] = None,
    pre_processors: typing.Tuple[CoProcessor] = None,
    post_processors: typing.Tuple[CoProcessor] = None
):
    warnings.warn(
        "migrate to ActionFactory that works as descriptor to aviod global db connection",
        DeprecationWarning
    )
    if 'default' not in meta.DATABASES:
        raise exceptions.NoDefaultDatabase()

    instance = action_class(
        meta.DATABASES['default'],
        event_processor,
        validators or tuple(),
        pre_processors or tuple(),
        post_processors or tuple()
    )

    return instance
