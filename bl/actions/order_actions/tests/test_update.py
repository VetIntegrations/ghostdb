import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ghostdb.db.models.order import Order, OrderStatus, OrderItem
from ghostdb.bl.actions.utils.base import action_factory
from ghostdb.bl.actions.utils.validators import ValidationError
from ..update import OrderUpdate, ItemUpdate


class TestOrderUpdate:

    @pytest.fixture(autouse=True)
    def setup_order(self, default_database):
        self.corporation = Corporation(name='Test Corporation 1')
        self.provider = Provider(first_name='John', last_name='Doe2')
        self.client = Client(first_name='John', last_name='Doe')
        self.pet = Pet(name='Ricky')
        self.order = Order(
            corporation=self.corporation,
            client=self.client,
            pet=self.pet,
            provider=self.provider,
            status=OrderStatus.open
        )

        default_database.add(self.corporation)
        default_database.add(self.provider)
        default_database.add(self.client)
        default_database.add(self.pet)
        default_database.add(self.order)
        default_database.commit()

    def test_ok(self, default_database):
        update_action = action_factory(OrderUpdate)

        new_status = OrderStatus.paid
        assert new_status != self.order.status

        self.order.status = new_status

        assert default_database.query(Order).count() == 1
        order, ok = update_action(self.order)
        assert ok
        assert order == self.order
        assert default_database.query(Order).count() == 1

        updated_order = default_database.query(Order)[0]
        assert updated_order.id == self.order.id
        assert updated_order.status == new_status

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.order import OrderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrderUpdate, 'process', process)

        with pytest.raises(Called):
            OrderAction.update(self.order)

    def test_update_right_record(self, default_database):
        pet2 = Pet(name='Ricky')
        order2 = Order(
            corporation=self.corporation,
            client=self.client,
            pet=pet2,
            provider=self.provider,
            status=OrderStatus.open
        )
        default_database.add(pet2)
        default_database.add(order2)

        update_action = action_factory(OrderUpdate)

        new_status = OrderStatus.void
        assert new_status != self.order.status

        self.order.status = new_status

        assert default_database.query(Order).count() == 2
        _, ok = update_action(self.order)
        assert ok
        assert default_database.query(Order).count() == 2

        updated_order = default_database.query(Order).filter(
            Order.id == self.order.id,
            Order.status == new_status,
            Order.pet == self.order.pet
        )
        assert updated_order.count() == 1

        stay_order = default_database.query(Order).filter(
            Order.id == order2.id,
            Order.status == order2.status,
            Order.pet == pet2
        )
        assert stay_order.count() == 1

    def test_validate_required_fields(self, default_database):
        from ghostdb.bl.actions.order import OrderAction

        self.order.pet = None

        with pytest.raises(ValidationError, match='Empty required fields: pet'):
            OrderAction.create(self.order)


class TestOrderItemUpdate:

    @pytest.fixture(autouse=True)
    def setup_order_item(self, default_database):
        self.corporation = Corporation(name='Test Corporation 1')
        self.provider = Provider(first_name='John', last_name='Doe2')
        self.client = Client(first_name='John', last_name='Doe')
        self.pet = Pet(name='Ricky')
        self.order = Order(
            corporation=self.corporation,
            client=self.client,
            pet=self.pet,
            provider=self.provider,
            status=OrderStatus.open
        )
        self.order_item = OrderItem(
            order=self.order,
            quantity=1,
            unit_price=3.14
        )

        default_database.add(self.corporation)
        default_database.add(self.provider)
        default_database.add(self.client)
        default_database.add(self.pet)
        default_database.add(self.order)
        default_database.add(self.order_item)
        default_database.commit()

    def test_ok(self, default_database):
        update_action = action_factory(ItemUpdate)

        new_quantity = 5
        assert new_quantity != self.order_item.quantity

        self.order_item.quantity = new_quantity

        assert default_database.query(OrderItem).count() == 1
        order_item, ok = update_action(self.order_item, self.order)
        assert ok
        assert order_item == self.order_item
        assert default_database.query(OrderItem).count() == 1

        updated_order_item = default_database.query(OrderItem)[0]
        assert updated_order_item.id == self.order_item.id
        assert updated_order_item.quantity == new_quantity

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.order import OrderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ItemUpdate, 'process', process)

        with pytest.raises(Called):
            OrderAction.update_item(self.order_item, self.order)

    def test_update_right_record(self, default_database):
        order_item2 = OrderItem(
            order_id=self.order.id,
            quantity=50,
            unit_price=0.15
        )
        default_database.add(order_item2)

        update_action = action_factory(ItemUpdate)

        new_quantity = 3
        assert new_quantity != self.order_item.quantity

        self.order_item.quantity = new_quantity

        assert default_database.query(OrderItem).count() == 2
        _, ok = update_action(self.order_item, self.order)
        assert ok
        assert default_database.query(OrderItem).count() == 2

        updated_order_item = default_database.query(OrderItem).filter(
            OrderItem.id == self.order_item.id,
            OrderItem.quantity == new_quantity
        )
        assert updated_order_item.count() == 1

        stay_order_item = default_database.query(OrderItem).filter(
            OrderItem.id == order_item2.id,
            OrderItem.quantity == order_item2.quantity
        )
        assert stay_order_item.count() == 1
