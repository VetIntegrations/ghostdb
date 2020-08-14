import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ghostdb.db.models.order import Order, OrderStatus, OrderItem
from ghostdb.bl.actions.utils.validators import ValidationError
from ghostdb.bl.actions.order import OrderAction
from ..create import OrderCreate, ItemCreate


class TestOrderCreate:

    @pytest.fixture(autouse=True)
    def setup(self, dbsession):
        self.corporation = Corporation(name='Test Corporation 1')
        self.provider = Provider(first_name='John', last_name='Doe2')
        self.client = Client(first_name='John', last_name='Doe')
        self.pet = Pet(name='Ricky')

        dbsession.add(self.corporation)
        dbsession.add(self.provider)
        dbsession.add(self.client)
        dbsession.add(self.pet)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        order = Order(
            corporation=self.corporation,
            client=self.client,
            pet=self.pet,
            provider=self.provider
        )

        with dbsession.no_autoflush:
            assert dbsession.query(Order).count() == 0
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_order, ok = action.create(order)
        assert ok
        assert new_order == order
        with dbsession.no_autoflush:
            assert dbsession.query(Order).count() == 1
            event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrderCreate, 'process', process)

        order = Order(
            corporation=self.corporation,
            client=self.client,
            pet=self.pet,
            provider=self.provider
        )
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(order)

    def test_validate_required_fields(self, dbsession, event_off):
        order = Order()

        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(ValidationError, match='Empty required fields: corporation'):
            action.create(order)


class TestOrderItemCreate:

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
        order_item = OrderItem(
            order_id=self.order.id,
            quantity=1,
            unit_price=3.14
        )

        assert dbsession.query(OrderItem).count() == 0
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_order_item, ok = action.add_item(order_item, self.order)
        assert ok
        assert new_order_item == order_item
        assert dbsession.query(OrderItem).count() == 1
        event_off.assert_called_once()

    def test_prefill_order(self, dbsession, event_off):
        order_item = OrderItem(
            order_id=self.order.id,
            quantity=1,
            unit_price=3.14
        )

        assert dbsession.query(OrderItem).count() == 0
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_order_item, ok = action.add_item(order_item, self.order)
        assert ok
        assert new_order_item == order_item
        assert new_order_item.order_id == self.order.id
        assert dbsession.query(OrderItem).count() == 1
        query_order_item = (
            dbsession
            .query(OrderItem)
            .filter(OrderItem.order == self.order)
        )
        assert query_order_item.count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch, event_off):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ItemCreate, 'process', process)

        order_item = OrderItem(
            order_id=self.order.id,
            quantity=1,
            unit_price=3.14
        )
        action = OrderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_item(order_item, self.order)
