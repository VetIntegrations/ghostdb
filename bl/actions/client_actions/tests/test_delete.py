import pytest

from ghostdb.db.models.client import (
    Client, ClientContact, ContactKind, ClientAddress, AddressKind
)
from ghostdb.bl.actions.utils.base import action_factory
from ..delete import ClientDelete, ContactDelete, AddressDelete


class TestClientDelete:

    @pytest.fixture(autouse=True)
    def setup_client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)

    def test_ok(self, default_database):
        delete_action = action_factory(ClientDelete)

        assert default_database.query(Client).count() == 1
        _, ok = delete_action(self.client)
        assert ok
        assert default_database.query(Client).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ClientDelete, 'process', process)

        with pytest.raises(Called):
            ClientAction.delete(self.client)

    def test_delete_right_record(self, default_database):
        client = Client(first_name='Jane', last_name='Doe')
        default_database.add(client)

        delete_action = action_factory(ClientDelete)

        assert default_database.query(Client).count() == 2
        _, ok = delete_action(self.client)
        assert ok
        assert default_database.query(Client).count() == 1

        assert default_database.query(Client)[0] == client


class TestClientContactDelete:

    @pytest.fixture(autouse=True)
    def setup_contact(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        self.contact = ClientContact(
            client=self.client,
            kind=ContactKind.home,
            value='+5874923'
        )
        default_database.add(self.client)
        default_database.add(self.contact)
        default_database.commit()

    def test_ok(self, default_database):
        delete_action = action_factory(ContactDelete)

        assert default_database.query(ClientContact).count() == 1
        _, ok = delete_action(self.contact, self.client)
        assert ok
        assert default_database.query(ClientContact).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactDelete, 'process', process)

        with pytest.raises(Called):
            ClientAction.remove_contact(self.contact, self.client)

    def test_delete_right_record(self, default_database):
        contact2 = ClientContact(
            client=self.client,
            kind=ContactKind.home,
            value='+48329482739'
        )
        default_database.add(contact2)

        delete_action = action_factory(ContactDelete)

        assert default_database.query(ClientContact).count() == 2
        _, ok = delete_action(self.contact, self.client)
        assert ok
        assert default_database.query(ClientContact).count() == 1

        assert default_database.query(ClientContact)[0] == contact2


class TestClientAddressDelete:

    @pytest.fixture(autouse=True)
    def setup_address(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        self.address = ClientAddress(
            client=self.client,
            kind=AddressKind.home,
            zip_code='00001'
        )
        default_database.add(self.client)
        default_database.add(self.address)
        default_database.commit()

    def test_ok(self, default_database):
        delete_action = action_factory(ContactDelete)

        assert default_database.query(ClientAddress).count() == 1
        _, ok = delete_action(self.address, self.client)
        assert ok
        assert default_database.query(ClientAddress).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AddressDelete, 'process', process)

        with pytest.raises(Called):
            ClientAction.remove_address(self.address, self.client)

    def test_delete_right_record(self, default_database):
        address2 = ClientAddress(
            client=self.client,
            kind=AddressKind.home,
            zip_code='00005'
        )
        default_database.add(address2)

        delete_action = action_factory(AddressDelete)

        assert default_database.query(ClientAddress).count() == 2
        _, ok = delete_action(self.address, self.client)
        assert ok
        assert default_database.query(ClientAddress).count() == 1

        assert default_database.query(ClientAddress)[0] == address2
