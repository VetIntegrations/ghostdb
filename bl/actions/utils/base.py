import abc
import typing
from collections import OrderedDict
from contextlib import contextmanager
from sqlalchemy.orm import session

from ghostdb.core.event import event, bus, data_dumper


CoProcessor = typing.Callable[[typing.Any, 'BaseAction'], bool]


class BaseActionSet:

    def __init__(
        self,
        db: session.Session,
        event_bus: bus.BaseEventBus,
        customer_name: str
    ):
        self.db = db
        self.event_bus = event_bus
        self.customer_name = customer_name


class BaseAction(abc.ABC):

    def __init__(
        self,
        db: session.Session,
        event: typing.Callable,
        validators: typing.Tuple[typing.Callable],
        pre_processors: typing.Tuple[CoProcessor],
        post_processors: typing.Tuple[CoProcessor],
        actionset: BaseActionSet
    ):
        self.db = db
        self.actionset = actionset
        self._event = event
        self._validators = validators
        self._pre_processors = pre_processors
        self._post_processors = post_processors
        self.__event_processing = True

    def validate(self, obj: typing.Any) -> bool:
        for validator in self._validators:
            validator(obj)

        return True

    def __call__(self, obj: typing.Any, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        self.validate(obj)

        ret = OrderedDict()
        for processor in self._pre_processors:
            ret[processor] = processor(obj, self)

        if self.__event_processing:
            self._event.register(self.actionset.customer_name, obj)

        obj, ret['process'] = self.process(obj, *args, **kwargs)

        if ret['process'] and self.__event_processing:
            self._event.trigger()

        for processor in self._post_processors:
            ret[processor] = processor(obj, self)

        return (obj, all(ret.values()))

    @contextmanager
    def discard_event(self):
        self.__event_processing = False
        yield self
        self.__event_processing = True

    @abc.abstractmethod
    def process(self, obj: typing.Any, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        ...


class EventFactory:

    def __init__(
        self,
        event_name: str,
        event_class: typing.Callable = event.InternalEvent,
        data_dumper: typing.Callable = data_dumper.GenericDataDumper
    ):
        self.event_class = event_class
        self.event_name = event_name
        self.data_dumper = data_dumper

    def __call__(self):
        return self.event_class(self.event_name, self.data_dumper)


class ActionFactory:

    def __init__(
        self,
        action_class: typing.Callable,
        event_factory: typing.Callable,
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
            db=actionset.db,
            event=event,
            validators=self.validators,
            pre_processors=self.pre_processors,
            post_processors=self.post_processors,
            actionset=actionset
        )
