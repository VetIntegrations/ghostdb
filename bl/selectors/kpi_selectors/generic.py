import typing
from datetime import datetime
from sqlalchemy import or_, orm
from sqlalchemy.orm.util import aliased

from ghostdb.db.models import order, corporation


def filter_successful_transactions(
    order_relation: orm.util.AliasedClass,
    query: orm.query.Query
) -> orm.query.Query:
    return query.filter(
        or_(
            ~order_relation.status.in_([
                order.OrderStatus.DELETED,
                order.OrderStatus.VOID
            ]),
            order_relation.status.is_(None)
        ),
    )


class KPISelectorGenericFilterMixin:

    def with_all_filters(
        self,
        corp: corporation.Corporation,
        datetime_from: datetime,
        datetime_to: datetime
    ) -> typing.Tuple[typing.Iterable[order.OrderItem], bool]:
        order_rel = aliased(order.Order)

        query, ok = self.process(order_rel=order_rel)
        query = self.selectorset.filter_orderitem_by_corporation(order_rel, query, corp)
        query = self.selectorset.filter_orderitem_by_timerange(query, datetime_from, datetime_to)

        return (query, True)
