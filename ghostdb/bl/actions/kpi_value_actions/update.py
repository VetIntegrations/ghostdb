import typing

from ghostdb.db.models import kpi
from ..utils import base


class KPIValueUpdate(base.BaseAction):

    def process(self, _kpi_value: kpi.AbstactKPIValue) -> typing.Tuple[kpi.AbstactKPIValue, bool]:
        self.db.add(_kpi_value)
        self.db.commit()

        return (_kpi_value, True)
