import uuid
import pytest

from ghostdb.db.models.order import Order, OrderStatus
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.provider import Provider
from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet
from ..order import OrderSelector


class TestByID:

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
        order, ok = OrderSelector(dbsession).by_id(self.order.id)

        assert ok
        assert order.id == self.order.id
        assert order.client == self.order.client

    def test_not_found(self, dbsession):
        order, ok = OrderSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert order is None
