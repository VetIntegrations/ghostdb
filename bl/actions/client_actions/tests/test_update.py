import pytest

from ghostdb.db.models.client import (
    Client, ClientContact, ContactKind, ClientAddress, AddressKind
)
from ghostdb.bl.actions.utils.base import action_factory
from ..update import ClientUpdate, ContactUpdate, AddressUpdate


class TestClientUpdate:

    @pytest.fixture(autouse=True)
    def setup_client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)

    def test_ok(self, default_database):
        update_action = action_factory(ClientUpdate)

        new_last_name = 'Krispi'
        assert new_last_name != self.client.last_name

        self.client.last_name = new_last_name

        assert default_database.query(Client).count() == 1
        client, ok = update_action(self.client)
        assert ok
        assert client == self.client
        assert default_database.query(Client).count() == 1

        updated_client = default_database.query(Client)[0]
        assert updated_client.id == self.client.id
        assert updated_client.last_name == new_last_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ClientUpdate, 'process', process)

        with pytest.raises(Called):
            ClientAction.update(self.client)

    def test_update_right_record(self, default_database):
        client = Client(first_name='Jane', last_name='Doe')
        default_database.add(client)

        update_action = action_factory(ClientUpdate)

        new_last_name = 'Ktulhu'
        assert new_last_name != self.client.last_name

        self.client.last_name = new_last_name

        assert default_database.query(Client).count() == 2
        _, ok = update_action(self.client)
        assert ok
        assert default_database.query(Client).count() == 2

        updated_client = default_database.query(Client).filter(
            Client.id == self.client.id,
            Client.last_name == new_last_name
        )
        assert updated_client.count() == 1

        stay_client = default_database.query(Client).filter(
            Client.id == client.id,
            Client.last_name == client.last_name
        )
        assert stay_client.count() == 1


class TestClientContactUpdate:

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
        update_action = action_factory(ContactUpdate)

        new_value = '+473829473'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert default_database.query(ClientContact).count() == 1
        contact, ok = update_action(self.contact, self.client)
        assert ok
        assert contact == self.contact
        assert default_database.query(ClientContact).count() == 1

        updated_contact = default_database.query(ClientContact)[0]
        assert updated_contact.id == self.contact.id
        assert updated_contact.value == new_value

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactUpdate, 'process', process)

        with pytest.raises(Called):
            ClientAction.update_contact(self.contact, self.client)

    def test_update_right_record(self, default_database):
        contact2 = ClientContact(
            client=self.client,
            kind=ContactKind.home,
            value='+483254794'
        )
        default_database.add(contact2)

        update_action = action_factory(ContactUpdate)

        new_value = '+9685749821'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert default_database.query(ClientContact).count() == 2
        _, ok = update_action(self.contact, self.client)
        assert ok
        assert default_database.query(ClientContact).count() == 2

        updated_contact = default_database.query(ClientContact).filter(
            ClientContact.id == self.contact.id,
            ClientContact.value == new_value
        )
        assert updated_contact.count() == 1

        stay_contact = default_database.query(ClientContact).filter(
            ClientContact.id == contact2.id,
            ClientContact.value == contact2.value
        )
        assert stay_contact.count() == 1


class TestClientAddressUpdate:

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
        update_action = action_factory(AddressUpdate)

        new_zip_code = '00002'
        assert new_zip_code != self.address.zip_code

        self.address.zip_code = new_zip_code

        assert default_database.query(ClientAddress).count() == 1
        address, ok = update_action(self.address, self.client)
        assert ok
        assert address == self.address
        assert default_database.query(ClientAddress).count() == 1

        updated_address = default_database.query(ClientAddress)[0]
        assert updated_address.id == self.address.id
        assert updated_address.zip_code == new_zip_code

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AddressUpdate, 'process', process)

        with pytest.raises(Called):
            ClientAction.update_address(self.address, self.client)

    def test_update_right_record(self, default_database):
        address2 = ClientAddress(
            client=self.client,
            kind=AddressKind.home,
            zip_code='00005'
        )
        default_database.add(address2)

        update_action = action_factory(AddressUpdate)

        new_zip_code = '00002'
        assert new_zip_code != self.address.zip_code

        self.address.zip_code = new_zip_code

        assert default_database.query(ClientAddress).count() == 2
        _, ok = update_action(self.address, self.client)
        assert ok
        assert default_database.query(ClientAddress).count() == 2

        updated_address = default_database.query(ClientAddress).filter(
            ClientAddress.id == self.address.id,
            ClientAddress.zip_code == new_zip_code
        )
        assert updated_address.count() == 1

        stay_address = default_database.query(ClientAddress).filter(
            ClientAddress.id == address2.id,
            ClientAddress.zip_code == address2.zip_code
        )
        assert stay_address.count() == 1
