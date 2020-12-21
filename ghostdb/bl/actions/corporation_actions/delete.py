import typing

from ghostdb.db.models import corporation
from ..utils import base


class Delete(base.BaseAction):

    def process(self, corp: corporation.Corporation) -> typing.Tuple[corporation.Corporation, bool]:
        self.db.delete(corp)
        self.db.commit()

        return (corp, True)


class DeleteMember(base.BaseAction):

    def process(self, member: corporation.Member) -> typing.Tuple[corporation.Member, bool]:
        self.db.delete(member)

        return (member, True)
