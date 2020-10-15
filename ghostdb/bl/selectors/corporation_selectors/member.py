import typing
import uuid

from ghostdb.db.models import corporation
from ..utils import base


class FindMemberByUserID(base.BaseSelector):

    def process(
        self,
        _corporation: corporation.Corporation,
        user_id: typing.Union[uuid.UUID, str]
    ) -> typing.Tuple[corporation.Member, bool]:
        query = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.corporation == _corporation,
                corporation.Member.user_id == user_id
            )
        )

        member = query.first()

        return (member, member is not None)


class ByInviteID(base.BaseSelector):

    def process(self, invite_id: str) -> typing.Tuple[corporation.Member, bool]:
        query = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.invite_id == invite_id
            )
        )

        member = query.first()

        return (member, member is not None)
