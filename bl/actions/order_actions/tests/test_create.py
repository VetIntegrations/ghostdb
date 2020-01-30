import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ghostdb.db.models.order import Order, OrderStatus, OrderItem
from ghostdb.bl.actions.utils.base import action_factory
from ghostdb.bl.actions.utils.validators import ValidationError
from ..create import OrderCreate, ItemCreate


class TestOrderCreate:

    @pytest.fixture(autouse=True)
    def setup(self, default_database):
        self.corporation = Corporation(name='Test Corporation 1')
        self.provider = Provider(first_name='John', last_name='Doe2')
        self.client = Client(first_name='John', last_name='Doe')
        self.pet = Pet(name='Ricky')

        default_database.add(self.corporation)
        default_database.add(self.provider)
        default_database.add(self.client)
        default_database.add(self.pet)
        default_database.commit()

    def test_ok(self, default_database):
        create_action = action_factory(OrderCreate)

        order = Order(
            corporation_id=self.corporation.id,
            client_id=self.client.id,
            pet_id=self.pet.id,
            provider_id=self.provider.id
        )

        assert default_database.query(Order).count() == 0
        new_order, ok = create_action(order)
        assert ok
        assert new_order == order
        assert default_database.query(Order).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.order import OrderAction

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
        with pytest.raises(Called):
            OrderAction.create(order)

    def test_validate_required_fields(self, default_database):
        from ghostdb.bl.actions.order import OrderAction

        order = Order()

        with pytest.raises(ValidationError, match='Empty required fields: corporation, client, pet, provider'):
            OrderAction.create(order)


class TestOrderItemCreate:

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
        create_action = action_factory(ItemCreate)

        order_item = OrderItem(
            order_id=self.order.id,
            quantity=1,
            unit_price=3.14
        )

        assert default_database.query(OrderItem).count() == 0
        new_order_item, ok = create_action(order_item, self.order)
        assert ok
        assert new_order_item == order_item
        assert default_database.query(OrderItem).count() == 1

    def test_prefill_order(self, default_database):
        create_action = action_factory(ItemCreate)

        order_item = OrderItem(
            order_id=self.order.id,
            quantity=1,
            unit_price=3.14
        )

        assert default_database.query(OrderItem).count() == 0
        new_order_item, ok = create_action(order_item, self.order)
        assert ok
        assert new_order_item == order_item
        assert new_order_item.order_id == self.order.id
        assert default_database.query(OrderItem).count() == 1
        query_order_item = (
            default_database
            .query(OrderItem)
            .filter(OrderItem.order == self.order)
        )
        assert query_order_item.count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.order import OrderAction

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
        with pytest.raises(Called):
            OrderAction.add_item(order_item, self.order)
