import typing

from ghostdb.db.models import corporation
from ..utils import base


class Create(base.BaseAction):

    def process(self, corp: corporation.Corporation) -> typing.Tuple[corporation.Corporation, bool]:
        self.db.add(corp)
        # self.db.commit()

        return (corp, True)
