import typing

from ghostdb.db.models import kpi
from ..utils import base


class KPIValueDelete(base.BaseAction):

    def process(self, _kpi_value: kpi.KPIValue) -> typing.Tuple[kpi.KPIValue, bool]:
        self.db.delete(_kpi_value)
        self.db.commit()

        return (_kpi_value, True)
