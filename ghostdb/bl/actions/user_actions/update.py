import typing
from datetime import datetime

from ghostdb.db.models import user
from ..utils import base


class UserUpdate(base.BaseAction):

    def process(self, _user: user.User) -> typing.Tuple[user.User, bool]:
        self.db.add(_user)
        self.db.commit()

        return (_user, True)


class MarkAsDeleted(base.BaseAction):

    def process(self, _user: user.User) -> typing.Tuple[user.User, bool]:
        _user.deleted = datetime.utcnow()

        self.db.add(_user)

        return (_user, True)


class UnmarkAsDeleted(base.BaseAction):

    def process(self, _user: user.User) -> typing.Tuple[user.User, bool]:
        _user.deleted = None

        self.db.add(_user)

        return (_user, True)
