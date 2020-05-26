from datetime import datetime
from sqlalchemy.orm.util import aliased

from ghostdb.db.models.order import Order, OrderItem, OrderStatus
from ghostdb.db.models.tests import factories
from ..generic import filter_successful_transactions


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
