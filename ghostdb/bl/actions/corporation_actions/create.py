import typing
from sqlalchemy_utils import Ltree

from ghostdb.db.models import corporation
from ..utils import base


class Create(base.BaseAction):

    def process(self, corp: corporation.Corporation) -> typing.Tuple[corporation.Corporation, bool]:
        self.db.add(corp)
        # self.db.commit()

        return (corp, True)


class AddMember(base.BaseAction):

    def process(
        self,
        corp: corporation.Corporation,
        member: corporation.Member,
        parent: corporation.Member = None,
    ) -> typing.Tuple[corporation.Member, bool]:
        member.corporation = corp

        if parent:
            if parent.path is None:
                member.path = Ltree(parent.id.hex)
            else:
                member.path = parent.path + Ltree(parent.id.hex)

        self.db.add(member)

        return (member, True)
