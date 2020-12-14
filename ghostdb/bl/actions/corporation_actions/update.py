import typing
import uuid
import pytz
from datetime import datetime
from sqlalchemy import not_

from ghostdb.db.models import corporation, user as user_model, security
from ..utils import base


class Update(base.BaseAction):

    def process(self, corp: corporation.Corporation) -> typing.Tuple[corporation.Corporation, bool]:
        self.db.add(corp)
        self.db.commit()

        return (corp, True)


class UpdateMember(base.BaseAction):

    def process(self, member: corporation.Member) -> typing.Tuple[corporation.Member, bool]:
        self.db.add(member)

        return (member, True)


class ActivateMember(base.BaseAction):

    def process(
        self,
        member: corporation.Member,
        invite: security.TemporaryToken = None,
        user: user_model.User = None
    ) -> typing.Tuple[corporation.Member, bool]:
        member.is_active = True
        member.date_of_join = datetime.utcnow().replace(tzinfo=pytz.UTC)

        if invite:
            ActivateMember.activate_by_invite(member, invite)
        else:
            ActivateMember.activate(member, user)

        self.db.add(member)

        return (member, True)

    @staticmethod
    def activate(
        member: corporation.Member,
        user: user_model.User
    ):
        member.user = user

    @staticmethod
    def activate_by_invite(
        member: corporation.Member,
        invite: security.TemporaryToken
    ):
        member.corporation_id = invite.extra['corporation']
        member.user.corporation_id = member.corporation_id
        member.invite = None
        member.user.date_of_join = member.date_of_join


class OrgChartRemoveUser(base.BaseAction):
    """Remove use from members of all corporations or corporation from args.
    You can filter out exact members as well."""

    def process(
        self,
        user: user_model.User,
        _corporation: corporation.Corporation = None,
        except_members: typing.Iterable[uuid.UUID] = None
    ) -> typing.Tuple[None, bool]:
        query = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.user_id == user.id
            )
        )
        if _corporation:
            query = query.filter(
                corporation.Member.corporation_id == _corporation.id
            )
        if except_members:
            query = query.filter(
                not_(corporation.Member.id.in_(except_members))
            )

        cnt = query.update(
            {
                corporation.Member.user_id: None,
            },
            synchronize_session=False
        )

        return (cnt, True)
