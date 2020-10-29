import typing

from ghostdb.db.models import user
from ..utils import base


class UserDelete(base.BaseAction):

    def process(self, _user: user.User) -> typing.Tuple[user.User, bool]:

        self.db.delete(_user)

        return (_user, True)
