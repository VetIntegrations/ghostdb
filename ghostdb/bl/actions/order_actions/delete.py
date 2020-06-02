import typing

from ghostdb.db.models import order
from ..utils import base


class OrderDelete(base.BaseAction):

    def process(self, _order: order.Order) -> typing.Tuple[order.Order, bool]:
        self.db.delete(_order)
        self.db.commit()

        return (_order, True)


class ItemDelete(base.BaseAction):

    def process(
        self,
        order_item: order.OrderItem,
        _order: order.Order
    ) -> typing.Tuple[order.OrderItem, bool]:
        assert order_item.order == _order

        self.db.delete(order_item)
        self.db.commit()

        return (order_item, True)
