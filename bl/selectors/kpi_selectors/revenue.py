import typing
from datetime import datetime
from sqlalchemy.orm.util import aliased

from ghostdb.db.models import corporation, order
from ..utils import base
from .generic import (
    filter_successful_transactions, filter_transation_timerange,
    filter_transation_corporation
)


class PMSGrossRevenueTransations(base.BaseSelector):

    def process(
        self,
        corp: corporation.Corporation,
        datetime_from: datetime,
        datetime_to: datetime
    ) -> typing.Tuple[typing.Iterable[order.OrderItem], bool]:
        order_rel = aliased(order.Order)
        query = self.db.query(order.OrderItem).join(order_rel)
        query = filter_transation_corporation(order_rel, query, corp)
        query = filter_successful_transactions(order_rel, query)
        query = filter_transation_timerange(query, datetime_from, datetime_to)

        return (query, True)
