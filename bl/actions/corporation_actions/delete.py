import typing

from ghostdb.db.models import corporation
from ..utils import base


class Delete(base.BaseAction):

    def process(self, corp: corporation.Corporation) -> typing.Tuple[corporation.Corporation, bool]:
        self.db.delete(corp)
        self.db.commit()

        return (corp, True)
