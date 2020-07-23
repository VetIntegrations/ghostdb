import abc
import typing


class BaseMessage(abc.ABC):

    @abc.abstractmethod
    def format(self) -> dict:
        ...


class InternalMessage(BaseMessage):

    def __init__(self, customer: str, event_name: str, obj: typing.Any, data: typing.Union[dict, None] = None):
        self.customer = customer
        self.event_name = event_name
        self.obj = obj
        self.data = data

    def format(self) -> dict:
        msg = {
            'customer': self.customer,
            'meta': {
                'event_name': self.event_name,
                'obj': {
                    'model': '.'.join((self.obj.__class__.__module__, self.obj.__class__.__name__, )),
                    'pk': self.obj.id.hex,
                },
            },
        }
        if self.data:
            msg['data'] = self.data.get_data_dump()

        return msg
