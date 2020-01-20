import uuid
import typing

from ghostdb.db.models import corporation
from ..utils import base


class ByID(base.BaseSelector):

    def process(self, id: uuid.UUID) -> typing.Tuple[corporation.Corporation, bool]:
        query = (
            self.db.query(corporation.Corporation)
            .filter(corporation.Corporation.id == id)
        )

        corp = query.first()

        return (corp, corp is not None)
