import uuid
import typing
from functools import partial
from sqlalchemy import func

from . import base


class ByID(base.BaseSelector):

    def process(self, pk: uuid.UUID) -> typing.Tuple[typing.Any, bool]:
        query = (
            self.db.query(self.model)
            .filter(self.model.id == pk)
        )

        obj = query.first()

        return (obj, obj is not None)


class ByPmsID(base.BaseSelector):

    def process(self, pk: uuid.UUID, customer_name: str, pms_name: str) -> typing.Tuple[typing.Any, bool]:
        query = (
            self.db.query(self.model).filter(
                self.model.__table__.c.pms_ids[customer_name][pms_name].as_string() == pk
            )
        )

        obj = query.first()

        return (obj, obj is not None)


class ByIName(base.BaseSelector):

    def process(self, name: str) -> typing.Tuple[typing.Any, bool]:
        query = (
            self.db.query(self.model)
            .filter(func.lower(self.model.name) == func.lower(name))
        )
        obj = query.first()

        return (obj, obj is not None)


class ByCustomField(base.BaseSelector):

    def __init__(self, *, filter_field: str, **kwargs):
        super().__init__(**kwargs)
        self.filter_field = filter_field

    def process(self, value: typing.Any, query=None) -> typing.Tuple[typing.Any, bool]:
        if query is None:
            query = self.db.query(self.model)

        query = query.filter(self.filter_field == value)

        return (query, True)

    @classmethod
    def factory(cls, filter_field: str) -> 'ByCustomField':
        return partial(cls, filter_field=filter_field)
