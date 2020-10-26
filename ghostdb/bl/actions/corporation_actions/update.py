import typing
import pytz
from datetime import datetime

from ghostdb.db.models import corporation
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
        corporation: corporation.Corporation = None
    ) -> typing.Tuple[corporation.Member, bool]:
        member.is_active = True
        member.date_of_join = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if corporation:
            member.corporation = corporation
        else:
            member.corporation_id = member.invite.extra['corporation']
        member.invite = None
        member.user.corporation_id = member.corporation_id
        member.user.date_of_join = member.date_of_join

        self.db.add(member)

        return (member, True)
