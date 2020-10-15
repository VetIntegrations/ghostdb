import os
import time
import typing
from hashlib import sha384

from ghostdb.db.models import security
from ..utils import base


class TemporaryTokenCreate(base.BaseAction):

    def process(self, token: security.TemporaryToken) -> typing.Tuple[security.TemporaryToken, bool]:
        if not token.token:
            digest = sha384(os.urandom(128) + str(time.time()).encode('utf-8'))
            token.token = digest.hexdigest()

        self.db.add(token)

        return (token, True)
