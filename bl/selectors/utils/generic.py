import uuid
import typing
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


class ByIName(base.BaseSelector):

    def process(self, name: str) -> typing.Tuple[typing.Any, bool]:
        query = (
            self.db.query(self.model)
            .filter(func.lower(self.model.name) == func.lower(name))
        )

        obj = query.first()

        return (obj, obj is not None)
