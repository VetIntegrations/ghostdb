import typing

from ghostdb.db.models import security
from ..utils import base


class TemporaryTokenDelete(base.BaseAction):

    def process(self, token: security.TemporaryToken) -> typing.Tuple[security.TemporaryToken, bool]:
        self.db.delete(token)
        self.db.commit()

        return (token, True)
