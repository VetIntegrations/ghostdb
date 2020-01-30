import abc
import typing
from collections import OrderedDict
from sqlalchemy.orm import session

from ghostdb.db import meta
from ghostdb import exceptions


CoProcessor = typing.Callable[[typing.Any, 'BaseAction'], bool]


class BaseAction(abc.ABC):

    def __init__(
        self,
        db: session.Session,
        validators: typing.Tuple[typing.Callable],
        # event processor (push to Pub/Sub notification)
        pre_processors: typing.Tuple[CoProcessor],
        post_processors: typing.Tuple[CoProcessor]
    ):
        self.db = db
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

        obj, ret['process'] = self.process(obj, *args, **kwargs)

        for processor in self._post_processors:
            ret[processor] = processor(obj, self)

        return (obj, all(ret.values()))

    @abc.abstractmethod
    def process(self, obj: typing.Any, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        ...


def action_factory(
    action_class: BaseAction,
    validators: typing.Tuple[typing.Callable] = None,
    pre_processors: typing.Tuple[CoProcessor] = None,
    post_processors: typing.Tuple[CoProcessor] = None
):
    if 'default' not in meta.DATABASES:
        raise exceptions.NoDefaultDatabase()

    instance = action_class(
        meta.DATABASES['default'],
        validators or tuple(),
        pre_processors or tuple(),
        post_processors or tuple()
    )

    return instance
