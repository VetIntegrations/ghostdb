import typing

from ghostdb.db.models import security
from ..utils import base


class TemporaryTokenUpdate(base.BaseAction):

    def process(self, token: security.TemporaryToken) -> typing.Tuple[security.TemporaryToken, bool]:
        self.db.add(token)

        return (token, True)
