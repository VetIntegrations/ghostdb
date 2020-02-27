import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ghostdb.db.models.order import Order, OrderStatus, OrderItem
from ghostdb.bl.actions.utils.validators import ValidationError
from ghostdb.bl.actions.order import OrderAction
from ..update import OrderUpdate, ItemUpdate


class TestOrderUpdate:

    @pytest.fixture(autouse=True)
    def setup_order(self, dbsession):
        self.corporation = Corporation(name='Test Corporation 1')
        self.provider = Provider(first_name='John', last_name='Doe2')
        self.client = Client(first_name='John', last_name='Doe')
        self.pet = Pet(name='Ricky')
        self.order = Order(
            corporation=self.corporation,
            client=self.client,
            pet=self.pet,
            provider=self.provider,
            status=OrderStatus.OPEN
        )

        dbsession.add(self.corporation)
        dbsession.add(self.provider)
        dbsession.add(self.client)
        dbsession.add(self.pet)
        dbsession.add(self.order)
        dbsession.commit()

    def test_ok(self, dbsession):
        new_status = OrderStatus.PAID
        assert new_status != self.order.status

        self.order.status = new_status

        assert dbsession.query(Order).count() == 1
        order, ok = OrderAction(dbsession).update(self.order)
        assert ok
        assert order == self.order
        assert dbsession.query(Order).count() == 1

        updated_order = dbsession.query(Order)[0]
        assert updated_order.id == self.order.id
        assert updated_order.status == new_status

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrderUpdate, 'process', process)

        with pytest.raises(Called):
            OrderAction(dbsession).update(self.order)

    def test_update_right_record(self, dbsession):
        pet2 = Pet(name='Ricky')
        order2 = Order(
            corporation=self.corporation,
            client=self.client,
            pet=pet2,
            provider=self.provider,
            status=OrderStatus.OPEN
        )
        dbsession.add(pet2)
        dbsession.add(order2)

        new_status = OrderStatus.VOID
        assert new_status != self.order.status

        self.order.status = new_status

        assert dbsession.query(Order).count() == 2
        _, ok = OrderAction(dbsession).update(self.order)
        assert ok
        assert dbsession.query(Order).count() == 2

        updated_order = dbsession.query(Order).filter(
            Order.id == self.order.id,
            Order.status == new_status,
            Order.pet == self.order.pet
        )
        assert updated_order.count() == 1

        stay_order = dbsession.query(Order).filter(
            Order.id == order2.id,
            Order.status == order2.status,
            Order.pet == pet2
        )
        assert stay_order.count() == 1

    def test_validate_required_fields(self, dbsession):
        self.order.client = None

        with pytest.raises(ValidationError, match='Empty required fields: client'):
            OrderAction(dbsession).create(self.order)


class TestOrderItemUpdate:

    @pytest.fixture(autouse=True)
    def setup_order_item(self, dbsession):
        self.corporation = Corporation(name='Test Corporation 1')
        self.provider = Provider(first_name='John', last_name='Doe2')
        self.client = Client(first_name='John', last_name='Doe')
        self.pet = Pet(name='Ricky')
        self.order = Order(
            corporation=self.corporation,
            client=self.client,
            pet=self.pet,
            provider=self.provider,
            status=OrderStatus.OPEN
        )
        self.order_item = OrderItem(
            order=self.order,
            quantity=1,
            unit_price=3.14
        )

        dbsession.add(self.corporation)
        dbsession.add(self.provider)
        dbsession.add(self.client)
        dbsession.add(self.pet)
        dbsession.add(self.order)
        dbsession.add(self.order_item)
        dbsession.commit()

    def test_ok(self, dbsession):
        new_quantity = 5
        assert new_quantity != self.order_item.quantity

        self.order_item.quantity = new_quantity

        assert dbsession.query(OrderItem).count() == 1
        order_item, ok = OrderAction(dbsession).update_item(self.order_item, self.order)
        assert ok
        assert order_item == self.order_item
        assert dbsession.query(OrderItem).count() == 1

        updated_order_item = dbsession.query(OrderItem)[0]
        assert updated_order_item.id == self.order_item.id
        assert updated_order_item.quantity == new_quantity

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ItemUpdate, 'process', process)

        with pytest.raises(Called):
            OrderAction(dbsession).update_item(self.order_item, self.order)

    def test_update_right_record(self, dbsession):
        order_item2 = OrderItem(
            order_id=self.order.id,
            quantity=50,
            unit_price=0.15
        )
        dbsession.add(order_item2)

        new_quantity = 3
        assert new_quantity != self.order_item.quantity

        self.order_item.quantity = new_quantity

        assert dbsession.query(OrderItem).count() == 2
        _, ok = OrderAction(dbsession).update_item(self.order_item, self.order)
        assert ok
        assert dbsession.query(OrderItem).count() == 2

        updated_order_item = dbsession.query(OrderItem).filter(
            OrderItem.id == self.order_item.id,
            OrderItem.quantity == new_quantity
        )
        assert updated_order_item.count() == 1

        stay_order_item = dbsession.query(OrderItem).filter(
            OrderItem.id == order_item2.id,
            OrderItem.quantity == order_item2.quantity
        )
        assert stay_order_item.count() == 1
