import typing
from sqlalchemy import orm, or_
from sqlalchemy.orm.util import aliased

from ghostdb.db.models import order
from ..utils import base
from .generic import KPISelectorGenericFilterMixin, filter_successful_transactions


class PMSGrossRevenueTransations(KPISelectorGenericFilterMixin, base.BaseSelector):

    def process(
        self, *, order_rel: orm.util.AliasedClass = None
    ) -> typing.Tuple[typing.Iterable[order.OrderItem], bool]:
        if order_rel is None:
            order_rel = aliased(order.Order)
        query = self.db.query(order.OrderItem).join(order_rel)
        query = filter_successful_transactions(order_rel, query)
        query = query.filter(
            ~order.OrderItem.is_inventory.is_(True),
            or_(
                ~order.OrderItem.description.ilike('%Refund%'),
                order.OrderItem.description.is_(None)
            )
        )

        return (query, True)
