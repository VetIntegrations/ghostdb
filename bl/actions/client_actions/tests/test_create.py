import pytest

from ghostdb.db.models.client import (
    Client, ClientContact, ContactKind, ClientAddress, AddressKind
)
from ghostdb.bl.actions.client import ClientAction
from ..create import ClientCreate, ContactCreate, AddressCreate


class TestClientCreate:

    def test_ok(self, dbsession, event_off):
        client = Client(first_name='John', last_name='Doe')

        act = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')

        assert len(act.create._event.messages) == 0
        assert dbsession.query(Client).count() == 0
        new_client, ok = act.create(client)
        assert ok
        assert new_client == client
        assert dbsession.query(Client).count() == 1

        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ClientCreate, 'process', process)

        client = Client(first_name='John', last_name='Doe')
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(client)


class TestClientContactCreate:

    @pytest.fixture(autouse=True)
    def setup_client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        dbsession.add(self.client)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        contact = ClientContact(
            client_id=self.client.id,
            kind=ContactKind.HOME,
            value='+4783294432'
        )

        act = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')

        assert len(act.create._event.messages) == 0
        assert dbsession.query(ClientContact).count() == 0
        new_contact, ok = act.add_contact(contact, self.client)
        assert ok
        assert new_contact == contact
        assert dbsession.query(ClientContact).count() == 1

        event_off.assert_called_once()

    def test_prefill_client(self, dbsession, event_off):
        contact = ClientContact(
            kind=ContactKind.HOME,
            value='+487329478932'
        )

        assert dbsession.query(ClientContact).count() == 0
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_contact, ok = action.add_contact(contact, self.client)
        assert ok
        assert new_contact == contact
        assert new_contact.client_id == self.client.id
        assert dbsession.query(ClientContact).count() == 1
        query_client_contact = (
            dbsession
            .query(ClientContact)
            .filter(ClientContact.client == self.client)
        )
        assert query_client_contact.count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactCreate, 'process', process)

        contact = ClientContact(
            client_id=self.client.id,
            kind=ContactKind.HOME,
            value='+327489327'
        )
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_contact(contact, self.client)


class TestClientAddressCreate:

    @pytest.fixture(autouse=True)
    def setup_client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        dbsession.add(self.client)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        address = ClientAddress(
            client_id=self.client.id,
            kind=AddressKind.home,
            zip_code='00001'
        )

        assert dbsession.query(ClientAddress).count() == 0
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_address, ok = action.add_address(address, self.client)
        assert ok
        assert new_address == address
        assert dbsession.query(ClientAddress).count() == 1

    def test_prefill_client(self, dbsession, event_off):
        address = ClientAddress(
            kind=AddressKind.home,
            zip_code='00001'
        )

        assert dbsession.query(ClientAddress).count() == 0
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_address, ok = action.add_address(address, self.client)
        assert ok
        assert new_address == address
        assert new_address.client_id == self.client.id
        assert dbsession.query(ClientAddress).count() == 1
        query_client_address = (
            dbsession
            .query(ClientAddress)
            .filter(ClientAddress.client == self.client)
        )
        assert query_client_address.count() == 1

    def test_action_class_use_right_action(self, dbsession, event_off, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AddressCreate, 'process', process)

        address = ClientAddress(
            client_id=self.client.id,
            kind=AddressKind.home,
            zip_code='00001'
        )
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_address(address, self.client)
