import typing

from ..utils import base


class ByName(base.BaseSelector):

    def process(self, name: str) -> typing.Tuple[typing.Any, bool]:
        query = (
            self.db.query(self.model)
            .filter(self.model.name == name)
        )

        obj = query.first()

        return (obj, obj is not None)
