import typing

from ghostdb.db.models import order
from ..utils import base


class OrderCreate(base.BaseAction):

    def process(self, _order: order.Order) -> typing.Tuple[order.Order, bool]:
        self.db.add(_order)
        self.db.commit()

        return (_order, True)


class ItemCreate(base.BaseAction):

    def process(
        self,
        order_item: order.OrderItem,
        _order: order.Order
    ) -> typing.Tuple[order.OrderItem, bool]:
        if order_item.order != _order or order_item.order_id != _order.id:
            order_item.order_id = _order.id

        self.db.add(order_item)
        self.db.commit()

        return (order_item, True)
