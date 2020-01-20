import abc
import typing
from sqlalchemy.orm import session


from ghostdb.db import meta
from ghostdb import exceptions


class BaseSelector(abc.ABC):

    def __init__(self, db: session.Session, model: meta.Base):
        self.db = db
        self.model = model

    def __call__(self, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        """Selector runner
        :returns: tuple with result and status (False on fail)
        """
        return self.process(*args, **kwargs)

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        ...


def selector_factory(selector_class: BaseSelector, model: meta.Base):
    if 'default' not in meta.DATABASES:
        raise exceptions.NoDefaultDatabase()

    instance = selector_class(
        meta.DATABASES['default'],
        model
    )

    return instance
