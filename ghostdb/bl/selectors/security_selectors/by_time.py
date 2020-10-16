import typing
from datetime import datetime, date
from sqlalchemy import func

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


class TemporaryTokenFilterByExpireDate(base.BaseSelector):

    def process(self, dt: date, kind: security.TokenKind = None) -> typing.Iterable[security.TemporaryToken]:
        query = (
            self.db.query(security.TemporaryToken)
            .filter(
                func.DATE(security.TemporaryToken.expires_at) == dt
            )
            .order_by(security.TemporaryToken.token)
        )

        if kind:
            query = query.filter(security.TemporaryToken.kind == kind)

        return query
