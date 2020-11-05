import uuid
import typing
from datetime import datetime

from ghostdb.db.models import security
from ..utils import base


class TemporatyTokenActiveByUser(base.BaseSelector):

    def process(self, user_id: uuid.UUID) -> typing.Iterable[security.TemporaryToken]:
        query = (
            self.db.query(security.TemporaryToken)
            .filter(
                security.TemporaryToken.user_id == user_id,
                security.TemporaryToken.expires_at > datetime.utcnow()
            )
        )

        return query
