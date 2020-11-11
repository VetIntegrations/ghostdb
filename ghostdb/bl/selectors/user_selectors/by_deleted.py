import typing
from datetime import datetime

from ghostdb.db.models import user
from ..utils import base


class FindDeletedUsers(base.BaseSelector):

    def process(
        self,
        dt: datetime,
    ) -> typing.Iterable[user.User]:
        query = (
            self.db.query(user.User)
            .filter(
                user.User.deleted < dt
            )
        )

        return query
