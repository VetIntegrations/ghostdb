import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ghostdb.db.models.order import Order, OrderStatus, OrderItem
from ghostdb.bl.actions.order import OrderAction
from ..delete import OrderDelete, ItemDelete


class TestOrderDelete:

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

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Order).count() == 1
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.order)
        assert ok
        assert dbsession.query(Order).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrderDelete, 'process', process)

        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.order)

    def test_delete_right_record(self, dbsession, event_off):
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

        assert dbsession.query(Order).count() == 2
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.order)
        assert ok
        assert dbsession.query(Order).count() == 1

        assert dbsession.query(Order)[0] == order2


class TestOrderItemDelete:

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

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(OrderItem).count() == 1
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.remove_item(self.order_item, self.order)
        assert ok
        assert dbsession.query(OrderItem).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ItemDelete, 'process', process)

        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.remove_item(self.order_item, self.order)

    def test_delete_right_record(self, dbsession, event_off):
        order_item2 = OrderItem(
            order_id=self.order.id,
            quantity=50,
            unit_price=0.15
        )
        dbsession.add(order_item2)

        assert dbsession.query(OrderItem).count() == 2
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.remove_item(self.order_item, self.order)
        assert ok
        assert dbsession.query(OrderItem).count() == 1

        assert dbsession.query(OrderItem)[0] == order_item2
