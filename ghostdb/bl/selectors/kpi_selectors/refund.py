import typing
from sqlalchemy import orm
from sqlalchemy.orm.util import aliased

from ghostdb.db.models import order
from ..utils import base
from .generic import KPISelectorGenericFilterMixin, filter_successful_transactions


class PMSRefundTransactions(KPISelectorGenericFilterMixin, base.BaseSelector):

    def process(
        self, *, order_rel: orm.util.AliasedClass = None
    ) -> typing.Tuple[typing.Iterable[order.OrderItem], bool]:
        if order_rel is None:
            order_rel = aliased(order.Order)
        query = self.db.query(order.OrderItem)
        query = filter_successful_transactions(order_rel, query)
        query = query.filter(
            order.OrderItem.amount < 0,
            order.OrderItem.description.ilike('%Refund%')
        )

        return (query, True)
