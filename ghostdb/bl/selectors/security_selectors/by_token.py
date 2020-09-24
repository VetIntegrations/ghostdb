import typing
from datetime import datetime

from ghostdb.db.models import security
from ..utils import base


class TemporaryTokenByTokenUtc(base.BaseSelector):

    def process(self, token: str) -> typing.Tuple[security.TemporaryToken, bool]:
        query = (
            self.db.query(security.TemporaryToken)
            .filter(
                security.TemporaryToken.token == token,
                security.TemporaryToken.expires_at > datetime.utcnow()
            )
        )

        _token = query.first()

        return (_token, _token is not None)
