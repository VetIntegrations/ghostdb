from datetime import datetime, timedelta
from sqlalchemy.orm.util import aliased

from ghostdb.db.models.order import Order, OrderItem, OrderStatus
from ghostdb.db.models.tests import factories
from ..generic import (
    filter_successful_transactions, filter_transation_timerange,
    filter_transation_corporation
)


def test_filter_successful_transactions(dbsession):
    for status in OrderStatus:
        order = factories.OrderFactory(status=status)
        factories.OrderItemFactory(
            order=order,
            quantity=100,
            unit_price=2,
            created_at=datetime.now()
        )
        factories.OrderItemFactory(
            order=order,
            quantity=100,
            unit_price=5,
            created_at=datetime.now()
        )

    order_rel = aliased(Order)
    query = dbsession.query(OrderItem).join(order_rel)
    assert query.count() == len(OrderStatus) * 2
    query = filter_successful_transactions(order_rel, query)
    assert query.count() == (len(OrderStatus) - 2) * 2
    statuses = {order_item.order.status for order_item in query}
    assert not statuses & {OrderStatus.DELETED, OrderStatus.VOID}


def test_filter_transation_timerange(dbsession):
    order = factories.OrderFactory()
    factories.OrderItemFactory(
        order=order,
        quantity=100,
        unit_price=2,
        created_at=datetime.now()
    )
    factories.OrderItemFactory(
        order=order,
        quantity=100,
        unit_price=5,
        created_at=datetime.now() - timedelta(days=1)
    )

    query = dbsession.query(OrderItem)
    assert query.count() == 2
    query = filter_transation_timerange(query, datetime.now().date(), datetime.now().date() + timedelta(days=1))
    assert query.count() == 1
    assert query[0].unit_price == 2


def test_filter_transation_corporation(dbsession):
    order_item1 = factories.OrderItemFactory(quantity=100, unit_price=2)
    order_item2 = factories.OrderItemFactory(quantity=100, unit_price=5)

    assert order_item1.order.corporation != order_item2.order.corporation

    order_rel = aliased(Order)
    query = dbsession.query(OrderItem).join(order_rel)
    assert query.count() == 2
    query = filter_transation_corporation(order_rel, query, order_item1.order.corporation)
    assert query.count() == 1
    assert query[0].unit_price == 2
