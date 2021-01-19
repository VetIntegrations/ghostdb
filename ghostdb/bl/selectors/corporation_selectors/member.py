import typing
import uuid
from sqlalchemy import func
from sqlalchemy.orm.util import aliased

from ghostdb.db.models import corporation, security
from ..utils import base


class FindMembersByUserID(base.BaseSelector):

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

        return query


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


class ActiveByUserID(base.BaseSelector):

    def process(
        self,
        user_id: typing.Union[uuid.UUID, str]
    ) -> typing.Tuple[corporation.Member, bool]:
        query = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.is_active.is_(True),
                corporation.Member.user_id == user_id
            )
        )

        member = query.first()

        return (member, member is not None)


class WithInviteForEmails(base.BaseSelector):

    def process(
        self,
        _corporation: corporation.Corporation,
        emails: typing.Iterable[str]
    ) -> typing.Tuple[typing.Iterable[corporation.Member], bool]:
        TempToken = aliased(security.TemporaryToken)
        query = (
            self.db.query(corporation.Member)
            .join(TempToken)
            .filter(
                corporation.Member.corporation == _corporation,
                TempToken.extra['email'].astext.in_(emails)
            )
        )

        return (query, True)


class OrgChart(base.BaseSelector):

    def process(
        self,
        corporation_id: typing.Union[uuid.UUID, str]
    ) -> typing.Tuple[typing.Iterable[corporation.Member], bool]:
        query = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.corporation_id == corporation_id
            )
            .order_by(
                func.coalesce(corporation.Member.path, '')
            )
        )

        return (query, True)
