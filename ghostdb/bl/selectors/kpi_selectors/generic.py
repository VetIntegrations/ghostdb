import typing
from datetime import datetime
from sqlalchemy import or_, orm
from sqlalchemy.orm.util import aliased

from ghostdb.db.models import order, corporation, payment


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

    def orderitem_with_all_filters(
        self,
        corp: corporation.Corporation,
        datetime_from: datetime,
        datetime_to: datetime,
        **kwargs
    ) -> typing.Tuple[typing.Iterable[order.OrderItem], bool]:
        if not kwargs.get('order_rel'):
            kwargs['order_rel'] = aliased(order.Order)

        query, ok = self.process(**kwargs)
        query = self.selectorset.filter_orderitem_by_business(kwargs['order_rel'], query, corp)
        query = self.selectorset.filter_orderitem_by_timerange(query, datetime_from, datetime_to)

        return (query, True)

    def orderitem_with_timerange_filter(
        self,
        datetime_from: datetime,
        datetime_to: datetime,
        **kwargs
    ) -> typing.Tuple[typing.Iterable[order.OrderItem], bool]:
        if not kwargs.get('order_rel'):
            kwargs['order_rel'] = aliased(order.Order)

        query, ok = self.process(**kwargs)
        query = self.selectorset.filter_orderitem_by_timerange(query, datetime_from, datetime_to)

        return (query, True)

    def payments_with_all_filters(
        self,
        corp: corporation.Corporation,
        datetime_from: datetime,
        datetime_to: datetime,
        **kwargs
    ) -> typing.Tuple[typing.Iterable[payment.Payment], bool]:

        query, ok = self.process(**kwargs)
        query = self.selectorset.filter_payments_by_business(query, corp)
        query = self.selectorset.filter_payments_by_timerange(query, datetime_from, datetime_to)

        return (query, True)
