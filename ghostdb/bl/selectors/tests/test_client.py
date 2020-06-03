import uuid
import pytest

from ghostdb.db.models.client import Client, ClientContact
from ..client import ClientSelector, ContactSelector


class TestClientByID:

    @pytest.fixture(autouse=True)
    def setup_client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        dbsession.add(self.client)
        dbsession.commit()

    def test_ok(self, dbsession):
        client, ok = ClientSelector(dbsession).by_id(self.client.id)

        assert ok
        assert client.id == self.client.id
        assert client.first_name == self.client.first_name
        assert client.last_name == self.client.last_name

    def test_not_found(self, dbsession):
        client, ok = ClientSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert client is None


class TestClientContactByID:

    @pytest.fixture(autouse=True)
    def setup_client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        self.contact = ClientContact(client=self.client, value='5674334')
        dbsession.add(self.client)
        dbsession.add(self.contact)
        dbsession.commit()

    def test_ok(self, dbsession):
        contact, ok = ContactSelector(dbsession).by_id(self.contact.id)

        assert ok
        assert contact.id == self.contact.id
        assert contact.value == self.contact.value

    def test_not_found(self, dbsession):
        contact, ok = ContactSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert contact is None
