import typing
import uuid
import pytz
from datetime import datetime
from sqlalchemy import not_
from sqlalchemy_utils.primitives import Ltree

from ghostdb.db.models import corporation, user as user_model, security
from ghostdb.bl.selectors.corporation import MemberSelector
from ..utils import base
from .ordering import MemberOrdering


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
        member.corporation_id = uuid.UUID(invite.extra['corporation'])
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


class OrgChartMoveMember(base.BaseAction):
    """Move member to new position"""

    def process(
        self,
        member: corporation.Member,
        new_parent: corporation.Member,
        left_neighbor: corporation.Member = None,
        right_neighbor: corporation.Member = None
    ) -> typing.Tuple[None, bool]:
        sql = '''
        UPDATE "{table_name}"
        SET
          "{column_name}" = (:new_parent_path)::ltree
            || subpath("{table_name}"."{column_name}", nlevel(:old_parent_path) - 1)
        WHERE
          "{column_name}" <@ :old_parent_path
        '''

        if new_parent.path:
            new_path = new_parent.path + Ltree(new_parent.id.hex)
        else:
            new_path = Ltree(new_parent.id.hex)

        self.db.execute(
            sql.format(
                table_name=corporation.Member.__tablename__,
                column_name=corporation.Member.path._query_clause_element().name,
            ),
            {
                'new_parent_path': new_path.path,
                'old_parent_path': (member.path + Ltree(member.id.hex)).path,
            }
        )

        member.path = new_path
        MemberOrdering(self.db).reorder(member, new_parent, left_neighbor, right_neighbor)

        self.db.add(member)

        return (member, True)


class RemoveUserFromMembers(base.BaseAction):

    def process(
        self,
        user: user_model.User,
    ):
        qs = MemberSelector(self.db).in_corporation_by_user_id(user.corporation, user.id)
        members = qs.update({corporation.Member.user_id: None})

        return (members, True)
