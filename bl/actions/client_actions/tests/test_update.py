import pytest

from ghostdb.db.models.client import (
    Client, ClientContact, ContactKind, ClientAddress, AddressKind
)
from ghostdb.bl.actions.client import ClientAction
from ..update import ClientUpdate, ContactUpdate, AddressUpdate


class TestClientUpdate:

    @pytest.fixture(autouse=True)
    def setup_client(self, dbsession):
        self.client = Client(first_name='John', last_name='Doe')
        dbsession.add(self.client)

    def test_ok(self, dbsession, event_off):
        new_last_name = 'Krispi'
        assert new_last_name != self.client.last_name

        self.client.last_name = new_last_name

        assert dbsession.query(Client).count() == 1
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        client, ok = action.update(self.client)
        assert ok
        assert client == self.client
        assert dbsession.query(Client).count() == 1
        event_off.assert_called_once()

        updated_client = dbsession.query(Client)[0]
        assert updated_client.id == self.client.id
        assert updated_client.last_name == new_last_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ClientUpdate, 'process', process)

        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.client)

    def test_update_right_record(self, dbsession, event_off):
        client = Client(first_name='Jane', last_name='Doe')
        dbsession.add(client)

        new_last_name = 'Ktulhu'
        assert new_last_name != self.client.last_name

        self.client.last_name = new_last_name

        assert dbsession.query(Client).count() == 2
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.client)
        assert ok
        assert dbsession.query(Client).count() == 2

        updated_client = dbsession.query(Client).filter(
            Client.id == self.client.id,
            Client.last_name == new_last_name
        )
        assert updated_client.count() == 1

        stay_client = dbsession.query(Client).filter(
            Client.id == client.id,
            Client.last_name == client.last_name
        )
        assert stay_client.count() == 1


class TestClientContactUpdate:

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
        new_value = '+473829473'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert dbsession.query(ClientContact).count() == 1
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        contact, ok = action.update_contact(self.contact, self.client)
        assert ok
        assert contact == self.contact
        assert dbsession.query(ClientContact).count() == 1

        updated_contact = dbsession.query(ClientContact)[0]
        assert updated_contact.id == self.contact.id
        assert updated_contact.value == new_value

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactUpdate, 'process', process)

        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update_contact(self.contact, self.client)

    def test_update_right_record(self, dbsession, event_off):
        contact2 = ClientContact(
            client=self.client,
            kind=ContactKind.HOME,
            value='+483254794'
        )
        dbsession.add(contact2)

        new_value = '+9685749821'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert dbsession.query(ClientContact).count() == 2
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update_contact(self.contact, self.client)
        assert ok
        assert dbsession.query(ClientContact).count() == 2

        updated_contact = dbsession.query(ClientContact).filter(
            ClientContact.id == self.contact.id,
            ClientContact.value == new_value
        )
        assert updated_contact.count() == 1

        stay_contact = dbsession.query(ClientContact).filter(
            ClientContact.id == contact2.id,
            ClientContact.value == contact2.value
        )
        assert stay_contact.count() == 1


class TestClientAddressUpdate:

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
        new_zip_code = '00002'
        assert new_zip_code != self.address.zip_code

        self.address.zip_code = new_zip_code

        assert dbsession.query(ClientAddress).count() == 1
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        address, ok = action.update_address(self.address, self.client)
        assert ok
        assert address == self.address
        assert dbsession.query(ClientAddress).count() == 1

        updated_address = dbsession.query(ClientAddress)[0]
        assert updated_address.id == self.address.id
        assert updated_address.zip_code == new_zip_code

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AddressUpdate, 'process', process)

        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update_address(self.address, self.client)

    def test_update_right_record(self, dbsession, event_off):
        address2 = ClientAddress(
            client=self.client,
            kind=AddressKind.home,
            zip_code='00005'
        )
        dbsession.add(address2)

        new_zip_code = '00002'
        assert new_zip_code != self.address.zip_code

        self.address.zip_code = new_zip_code

        assert dbsession.query(ClientAddress).count() == 2
        action = ClientAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update_address(self.address, self.client)
        assert ok
        assert dbsession.query(ClientAddress).count() == 2

        updated_address = dbsession.query(ClientAddress).filter(
            ClientAddress.id == self.address.id,
            ClientAddress.zip_code == new_zip_code
        )
        assert updated_address.count() == 1

        stay_address = dbsession.query(ClientAddress).filter(
            ClientAddress.id == address2.id,
            ClientAddress.zip_code == address2.zip_code
        )
        assert stay_address.count() == 1
