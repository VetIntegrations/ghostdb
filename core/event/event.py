import abc
import logging

from . import message, bus, exceptions


logger = logging.getLogger('ghostdb.event')


EVENT_RECORD_CREATE = 'record.create'
EVENT_RECORD_UPDATE = 'record.update'
EVENT_RECORD_DELETE = 'record.delete'


class BaseEvent(abc.ABC):

    def __init__(self, event_name: str, data_dumper):
        self.name = event_name
        self.data_dumper = data_dumper
        self.messages = []
        self.event_bus = None

    def set_event_bus(self, event_bus):
        self.event_bus = event_bus

    def check_event_bus(self):
        if self.event_bus is None or not isinstance(self.event_bus, bus.BaseEventBus):
            raise exceptions.MissingEventBusException()

    @abc.abstractmethod
    def register(self, customer: str, obj):
        ...

    def trigger(self):
        self.check_event_bus()

        for msg in self.messages[::]:
            self.event_bus.publish(msg)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            self.trigger()
        elif self.messages:
            logger.error(
                'event messages would not be send because of process exception: %s',
                exc_type
            )


class InternalEvent(BaseEvent):

    def register(self, customer: str, obj):
        print('!!!', obj)
        msg = message.InternalMessage(
            customer=customer,
            event_name=self.name,
            obj=obj,
            data=self.data_dumper(obj)
        )
        self.messages.append(msg)
