import typing
import uuid
import pytz
from datetime import datetime
from sqlalchemy import not_
from sqlalchemy_utils.primitives import Ltree

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
        self._reorder(member, new_parent, left_neighbor, right_neighbor)

        self.db.add(member)

        return (member, True)

    def _reorder(
        self,
        member: corporation.Member,
        new_parent: corporation.Member = None,
        left_neighbor: corporation.Member = None,
        right_neighbor: corporation.Member = None
    ):
        if left_neighbor and right_neighbor:
            self._reorder_by_both_neighbors(member, left_neighbor, right_neighbor)
        elif left_neighbor:
            self._reorder_by_left_neighbor(member, left_neighbor)
        elif right_neighbor:
            self._reorder_by_right_neighbor(member, right_neighbor)
        elif new_parent:
            self._reorder_member_set_most_left(member)

    def _reorder_by_both_neighbors(
        self,
        member: corporation.Member,
        left_neighbor: corporation.Member = None,
        right_neighbor: corporation.Member = None
    ):
        def calc_position(start_ordering, left_neighbor, right_neighbor):
            return (
                min_ordering
                + abs((right_neighbor.ordering - left_neighbor.ordering) // 2)
            )

        min_ordering = min(right_neighbor.ordering, left_neighbor.ordering)
        position = calc_position(min_ordering, left_neighbor, right_neighbor)
        if position != right_neighbor.ordering and position != left_neighbor.ordering:
            member.ordering = position
        else:
            self._reorder__shift_right(left_neighbor, right_neighbor.ordering)
            member.ordering = calc_position(min_ordering, left_neighbor, right_neighbor)

    def _reorder_by_left_neighbor(
        self,
        member: corporation.Member,
        left_neighbor: corporation.Member = None
    ):
        right_neighbor = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.path == left_neighbor.path,
                corporation.Member.ordering > left_neighbor.ordering,
                corporation.Member.id != member.id
            )
            .order_by(corporation.Member.ordering.asc())
            .first()
        )
        if right_neighbor:
            self._reorder_by_both_neighbors(member, left_neighbor, right_neighbor)
        else:
            member.ordering = left_neighbor.ordering + 100

    def _reorder_by_right_neighbor(
        self,
        member: corporation.Member,
        right_neighbor: corporation.Member = None
    ):
        left_neighbor = (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.path == right_neighbor.path,
                corporation.Member.ordering < right_neighbor.ordering,
                corporation.Member.id != member.id
            )
            .order_by(corporation.Member.ordering.desc())
            .first()
        )
        if left_neighbor:
            self._reorder_by_both_neighbors(member, left_neighbor, right_neighbor)
        else:
            self._reorder_member_set_most_left(member)

    def _reorder_member_set_most_left(self, member: corporation.Member):
        self._reorder__shift_right(member, 0)
        member.ordering = 0

    def _reorder__shift_right(self, member: corporation.Member, min_ordering: int):
        (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.id != member.id,
                corporation.Member.path == member.path,
                corporation.Member.ordering >= min_ordering
            )
            .update({
                corporation.Member.ordering: corporation.Member.ordering + 100,
            })
        )
