import pytest

from ghostdb.db.models.client import (
    Client, ClientContact, ContactKind, ClientAddress, AddressKind
)
from ghostdb.bl.actions.utils.base import action_factory
from ..create import ClientCreate, ContactCreate, AddressCreate


class TestClientCreate:

    def test_ok(self, default_database):
        create_action = action_factory(ClientCreate)

        client = Client(first_name='John', last_name='Doe')

        assert default_database.query(Client).count() == 0
        new_client, ok = create_action(client)
        assert ok
        assert new_client == client
        assert default_database.query(Client).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ClientCreate, 'process', process)

        client = Client(first_name='John', last_name='Doe')
        with pytest.raises(Called):
            ClientAction.create(client)


class TestClientContactCreate:

    @pytest.fixture(autouse=True)
    def setup_client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)
        default_database.commit()

    def test_ok(self, default_database):
        create_action = action_factory(ContactCreate)

        contact = ClientContact(
            client_id=self.client.id,
            kind=ContactKind.home,
            value='+4783294432'
        )

        assert default_database.query(ClientContact).count() == 0
        new_contact, ok = create_action(contact, self.client)
        assert ok
        assert new_contact == contact
        assert default_database.query(ClientContact).count() == 1

    def test_prefill_client(self, default_database):
        create_action = action_factory(ContactCreate)

        contact = ClientContact(
            kind=ContactKind.home,
            value='+487329478932'
        )

        assert default_database.query(ClientContact).count() == 0
        new_contact, ok = create_action(contact, self.client)
        assert ok
        assert new_contact == contact
        assert new_contact.client_id == self.client.id
        assert default_database.query(ClientContact).count() == 1
        query_client_contact = (
            default_database
            .query(ClientContact)
            .filter(ClientContact.client == self.client)
        )
        assert query_client_contact.count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactCreate, 'process', process)

        contact = ClientContact(
            client_id=self.client.id,
            kind=ContactKind.home,
            value='+327489327'
        )
        with pytest.raises(Called):
            ClientAction.add_contact(contact, self.client)


class TestClientAddressCreate:

    @pytest.fixture(autouse=True)
    def setup_client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)
        default_database.commit()

    def test_ok(self, default_database):
        create_action = action_factory(AddressCreate)

        address = ClientAddress(
            client_id=self.client.id,
            kind=AddressKind.home,
            zip_code='00001'
        )

        assert default_database.query(ClientAddress).count() == 0
        new_address, ok = create_action(address, self.client)
        assert ok
        assert new_address == address
        assert default_database.query(ClientAddress).count() == 1

    def test_prefill_client(self, default_database):
        create_action = action_factory(ContactCreate)

        address = ClientAddress(
            kind=AddressKind.home,
            zip_code='00001'
        )

        assert default_database.query(ClientAddress).count() == 0
        new_address, ok = create_action(address, self.client)
        assert ok
        assert new_address == address
        assert new_address.client_id == self.client.id
        assert default_database.query(ClientAddress).count() == 1
        query_client_address = (
            default_database
            .query(ClientAddress)
            .filter(ClientAddress.client == self.client)
        )
        assert query_client_address.count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

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
        with pytest.raises(Called):
            ClientAction.add_address(address, self.client)
