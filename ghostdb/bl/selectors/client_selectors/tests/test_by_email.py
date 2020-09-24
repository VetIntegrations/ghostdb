import pytest

from ghostdb.db.models.client import Client
from ..by_email import ByEmail


class TestClientSelectByEmail:

    @pytest.fixture(autouse=True)
    def client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe', email='john@doe.local')
        dbsession.add(self.client)

    def test_ok(self, dbsession):
        selector = ByEmail(dbsession, Client, None)

        assert dbsession.query(Client).count() == 1
        client, ok = selector(self.client.email)
        assert ok
        assert client == self.client

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.client import ClientSelector

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ByEmail, 'process', process)

        with pytest.raises(Called):
            ClientSelector(dbsession).by_email(self.client.email)

    def test_get_right_record(self, dbsession):
        client2 = Client(first_name='Jane', last_name='Doe', email='jane@doe.local')
        dbsession.add(client2)

        selector = ByEmail(dbsession, Client, None)

        assert dbsession.query(Client).count() == 2
        client, ok = selector(self.client.email)
        assert ok
        assert client == self.client
