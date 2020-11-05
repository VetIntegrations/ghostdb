import uuid
import typing
from datetime import datetime

from ghostdb.db.models import security
from ..utils import base


class TemporaryTokenByUserUtc(base.BaseSelector):

    def process(self, user_id: uuid.UUID) -> typing.Tuple[security.TemporaryToken, bool]:
        query = (
            self.db.query(security.TemporaryToken)
            .filter(
                security.TemporaryToken.user_id == user_id,
                security.TemporaryToken.expires_at > datetime.utcnow()
            )
        )
        token = query.first()

        return (token, token is not None)
