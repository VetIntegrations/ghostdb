import typing

from ghostdb.db.models import user
from ..utils import base


class UserCreate(base.BaseAction):

    def process(self, _user: user.User) -> typing.Tuple[user.User, bool]:
        self.db.add(_user)
        # self.db.commit()

        return (_user, True)
