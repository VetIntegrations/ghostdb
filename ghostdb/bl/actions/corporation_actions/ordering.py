from sqlalchemy.orm import session
from sqlalchemy_utils.primitives import Ltree

from ghostdb.db.models import corporation


class MemberOrdering:
    ORDERING_STEP = 100

    def __init__(self, db: session.Session):
        self.db = db

    def reorder_member_substitute_by_subordinates(self, member: corporation.Member):
        subordinates = (
            self.db.query(corporation.Member)
            .filter(corporation.Member.path == member.path + Ltree(member.id.hex))
            .order_by(corporation.Member.ordering.asc())
        )

        if subordinates.count():
            self._reorder__shift_right(
                member,
                member.ordering + 1,
                (subordinates.count() - 1) * self.ORDERING_STEP
            )

            for idx, (subordinate) in enumerate(subordinates):
                subordinate.ordering = member.ordering + self.ORDERING_STEP * idx

    def reorder(
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
            member.ordering = left_neighbor.ordering + self.ORDERING_STEP

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

    def _reorder__shift_right(self, member: corporation.Member, min_ordering: int, offset: int = None):
        if not offset:
            offset = self.ORDERING_STEP

        (
            self.db.query(corporation.Member)
            .filter(
                corporation.Member.id != member.id,
                corporation.Member.path == member.path,
                corporation.Member.ordering >= min_ordering
            )
            .update({
                corporation.Member.ordering: corporation.Member.ordering + offset,
            })
        )
