import typing
from datetime import datetime

from sqlalchemy import or_

from ghostdb.db.models.user import User
from ghostdb.db.models.security import TemporaryToken
from ..utils import base


class FindNotVerificationUsers(base.BaseSelector):

    def process(
        self,
    ) -> typing.Iterable[User]:

        query = (
            self.db.query(User).outerjoin(TemporaryToken, User.id == TemporaryToken.user_id)
            .filter(
                User.is_ghost.is_(True),
                or_(
                    TemporaryToken.expires_at <= datetime.utcnow(),
                    TemporaryToken.token.is_(None)
                )
            )
        )

        return query
