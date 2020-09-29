import typing

from ghostdb.db.models import user
from ..utils import base


class ByEmail(base.BaseSelector):

    def process(self, value: str) -> typing.Tuple[user.User, bool]:
        query = (
            self.db.query(user.User)
            .filter(user.User.email == value)
        )

        _user = query.first()

        return (_user, _user is not None)
