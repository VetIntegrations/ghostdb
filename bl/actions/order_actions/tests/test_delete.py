import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ghostdb.db.models.order import Order, OrderStatus, OrderItem
from ghostdb.bl.actions.utils.base import action_factory
from ..delete import OrderDelete, ItemDelete


class TestOrderDelete:

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
        delete_action = action_factory(OrderDelete)

        assert default_database.query(Order).count() == 1
        _, ok = delete_action(self.order)
        assert ok
        assert default_database.query(Order).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.order import OrderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrderDelete, 'process', process)

        with pytest.raises(Called):
            OrderAction.delete(self.order)

    def test_delete_right_record(self, default_database):
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

        delete_action = action_factory(OrderDelete)

        assert default_database.query(Order).count() == 2
        _, ok = delete_action(self.order)
        assert ok
        assert default_database.query(Order).count() == 1

        assert default_database.query(Order)[0] == order2


class TestOrderItemDelete:

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
        delete_action = action_factory(ItemDelete)

        assert default_database.query(OrderItem).count() == 1
        _, ok = delete_action(self.order_item, self.order)
        assert ok
        assert default_database.query(OrderItem).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.order import OrderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ItemDelete, 'process', process)

        with pytest.raises(Called):
            OrderAction.remove_item(self.order_item, self.order)

    def test_delete_right_record(self, default_database):
        order_item2 = OrderItem(
            order_id=self.order.id,
            quantity=50,
            unit_price=0.15
        )
        default_database.add(order_item2)

        delete_action = action_factory(ItemDelete)

        assert default_database.query(OrderItem).count() == 2
        _, ok = delete_action(self.order_item, self.order)
        assert ok
        assert default_database.query(OrderItem).count() == 1

        assert default_database.query(OrderItem)[0] == order_item2
