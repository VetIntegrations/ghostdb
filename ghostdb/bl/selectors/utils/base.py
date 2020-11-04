import abc
import typing
import warnings
from sqlalchemy.orm import session


from ghostdb.db import meta
from ghostdb import exceptions


class BaseSelectorSet:

    def __init__(self, db: session.Session):
        self.db = db


class BaseSelector(abc.ABC):

    def __init__(self, db: session.Session, model: meta.Base, selectorset: BaseSelectorSet):
        self.db = db
        self.model = model
        self.selectorset = selectorset

    def __call__(self, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        """Selector runner
        :returns: tuple with result and status (False on fail)
        """
        return self.process(*args, **kwargs)

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> typing.Tuple[typing.Any, bool]:
        ...


class SelectorFactory:

    def __init__(self, selector_class: BaseSelector, model: meta.Base):
        self.selector_class = selector_class
        self.model = model

    def __get__(self, selectorset, _type):
        if not issubclass(_type, BaseSelectorSet):
            raise AttributeError(f'{_type} should be inherited from BaseSelectorSet')

        return self.selector_class(
            db=selectorset.db,
            model=self.model,
            selectorset=selectorset
        )


def selector_factory(selector_class: BaseSelector, model: meta.Base):
    warnings.warn(
        "migrate to SelectorFactory that works as descriptor to aviod global db connection",
        DeprecationWarning
    )
    if 'default' not in meta.DATABASES:
        raise exceptions.NoDefaultDatabase()

    instance = selector_class(
        meta.DATABASES['default'],
        model
    )

    return instance
