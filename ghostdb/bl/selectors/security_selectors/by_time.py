import typing
from datetime import datetime

from ghostdb.db.models import security
from ..utils import base


class TemporaryTokenExpired(base.BaseSelector):

    def process(self) -> typing.Iterable[security.TemporaryToken]:
        query = (
            self.db.query(security.TemporaryToken)
            .filter(
                security.TemporaryToken.expires_at < datetime.utcnow()
            )
        )

        return query
