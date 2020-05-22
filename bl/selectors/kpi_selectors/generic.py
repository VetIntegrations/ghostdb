from datetime import datetime
from sqlalchemy import or_, orm
from ghostdb.db.models import order, corporation


def filter_transation_corporation(
    order_relation: orm.util.AliasedClass,
    query: orm.query.Query,
    corp: corporation.Corporation
) -> orm.query.Query:
    return query.filter(
        order_relation.corporation == corp
    )


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


def filter_transation_timerange(
    query: orm.query.Query,
    datetime_from: datetime,
    datetime_to: datetime
) -> orm.query.Query:
    return query.filter(
        order.OrderItem.created_at >= datetime_from,
        order.OrderItem.created_at < datetime_to,
    )
