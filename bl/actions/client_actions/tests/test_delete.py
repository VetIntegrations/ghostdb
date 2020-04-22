import pytest

from ghostdb.db.models.client import (
    Client, ClientContact, ContactKind, ClientAddress, AddressKind
)
from ghostdb.bl.actions.client import ClientAction
from ..delete import ClientDelete, ContactDelete, AddressDelete


class TestClientDelete:

    @pytest.fixture(autouse=True)
    def setup_client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        dbsession.add(self.client)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Client).count() == 1
        _, ok = ClientAction(dbsession).delete(self.client)
        assert ok
        assert dbsession.query(Client).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ClientDelete, 'process', process)

        with pytest.raises(Called):
            ClientAction(dbsession).delete(self.client)

    def test_delete_right_record(self, dbsession, event_off):
        client = Client(first_name='Jane', last_name='Doe')
        dbsession.add(client)

        assert dbsession.query(Client).count() == 2
        _, ok = ClientAction(dbsession).delete(self.client)
        assert ok
        assert dbsession.query(Client).count() == 1

        assert dbsession.query(Client)[0] == client


class TestClientContactDelete:

    @pytest.fixture(autouse=True)
    def setup_contact(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        self.contact = ClientContact(
            client=self.client,
            kind=ContactKind.HOME,
            value='+5874923'
        )
        dbsession.add(self.client)
        dbsession.add(self.contact)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(ClientContact).count() == 1
        _, ok = ClientAction(dbsession).remove_contact(self.contact, self.client)
        assert ok
        assert dbsession.query(ClientContact).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactDelete, 'process', process)

        with pytest.raises(Called):
            ClientAction(dbsession).remove_contact(self.contact, self.client)

    def test_delete_right_record(self, dbsession, event_off):
        contact2 = ClientContact(
            client=self.client,
            kind=ContactKind.HOME,
            value='+48329482739'
        )
        dbsession.add(contact2)

        assert dbsession.query(ClientContact).count() == 2
        _, ok = ClientAction(dbsession).remove_contact(self.contact, self.client)
        assert ok
        assert dbsession.query(ClientContact).count() == 1

        assert dbsession.query(ClientContact)[0] == contact2


class TestClientAddressDelete:

    @pytest.fixture(autouse=True)
    def setup_address(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        self.address = ClientAddress(
            client=self.client,
            kind=AddressKind.home,
            zip_code='00001'
        )
        dbsession.add(self.client)
        dbsession.add(self.address)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(ClientAddress).count() == 1
        _, ok = ClientAction(dbsession).remove_address(self.address, self.client)
        assert ok
        assert dbsession.query(ClientAddress).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AddressDelete, 'process', process)

        with pytest.raises(Called):
            ClientAction(dbsession).remove_address(self.address, self.client)

    def test_delete_right_record(self, dbsession, event_off):
        address2 = ClientAddress(
            client=self.client,
            kind=AddressKind.home,
            zip_code='00005'
        )
        dbsession.add(address2)

        assert dbsession.query(ClientAddress).count() == 2
        _, ok = ClientAction(dbsession).remove_address(self.address, self.client)
        assert ok
        assert dbsession.query(ClientAddress).count() == 1

        assert dbsession.query(ClientAddress)[0] == address2
