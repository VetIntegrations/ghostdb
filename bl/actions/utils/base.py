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
        # event processor (push to Pub/Sub notification)
        pre_processors: typing.List[CoProcessor],
        post_processors: typing.List[CoProcessor]
    ):
        self.db = db
        self._pre_processors = pre_processors
        self._post_processors = post_processors

    def __call__(self, obj: typing.Any, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
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
    pre_processors: typing.List[CoProcessor],
    post_processors: typing.List[CoProcessor]
):
    if 'default' not in meta.DATABASES:
        raise exceptions.NoDefaultDatabase()

    instance = action_class(
        meta.DATABASES['default'],
        pre_processors,
        post_processors
    )

    return instance
