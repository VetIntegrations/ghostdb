import uuid
import typing

from . import base


class ByID(base.BaseSelector):

    def process(self, pk: uuid.UUID) -> typing.Tuple[typing.Any, bool]:
        query = (
            self.db.query(self.model)
            .filter(self.model.id == pk)
        )

        obj = query.first()

        return (obj, obj is not None)
