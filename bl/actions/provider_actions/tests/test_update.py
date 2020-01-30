import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ContactKind
from ghostdb.bl.actions.utils.base import action_factory
from ..update import ProviderUpdate, ContactUpdate


class TestProviderUpdate:

    @pytest.fixture(autouse=True)
    def setup_provider(self, default_database):
        self.provider = Provider(first_name='John', last_name='Doe')
        default_database.add(self.provider)

    def test_ok(self, default_database):
        update_action = action_factory(ProviderUpdate)

        new_last_name = 'Krispi'
        assert new_last_name != self.provider.last_name

        self.provider.last_name = new_last_name

        assert default_database.query(Provider).count() == 1
        provider, ok = update_action(self.provider)
        assert ok
        assert provider == self.provider
        assert default_database.query(Provider).count() == 1

        updated_provider = default_database.query(Provider)[0]
        assert updated_provider.id == self.provider.id
        assert updated_provider.last_name == new_last_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.provider import ProviderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderUpdate, 'process', process)

        with pytest.raises(Called):
            ProviderAction.update(self.provider)

    def test_update_right_record(self, default_database):
        provider2 = Provider(first_name='Jane', last_name='Doe')
        default_database.add(provider2)

        update_action = action_factory(ProviderUpdate)

        new_last_name = 'Ktulhu'
        assert new_last_name != self.provider.last_name

        self.provider.last_name = new_last_name

        assert default_database.query(Provider).count() == 2
        _, ok = update_action(self.provider)
        assert ok
        assert default_database.query(Provider).count() == 2

        updated_provider = default_database.query(Provider).filter(
            Provider.id == self.provider.id,
            Provider.last_name == new_last_name
        )
        assert updated_provider.count() == 1

        stay_provider = default_database.query(Provider).filter(
            Provider.id == provider2.id,
            Provider.last_name == provider2.last_name
        )
        assert stay_provider.count() == 1


class TestProviderContactUpdate:

    @pytest.fixture(autouse=True)
    def setup_contact(self, default_database):
        self.provider = Provider(first_name='John', last_name='Doe')
        self.contact = ProviderContact(
            provider=self.provider,
            kind=ContactKind.phone,
            value='+5874923'
        )
        default_database.add(self.provider)
        default_database.add(self.contact)
        default_database.commit()

    def test_ok(self, default_database):
        update_action = action_factory(ContactUpdate)

        new_value = '+473829473'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert default_database.query(ProviderContact).count() == 1
        contact, ok = update_action(self.contact, self.provider)
        assert ok
        assert contact == self.contact
        assert default_database.query(ProviderContact).count() == 1

        updated_contact = default_database.query(ProviderContact)[0]
        assert updated_contact.id == self.contact.id
        assert updated_contact.value == new_value

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.provider import ProviderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactUpdate, 'process', process)

        with pytest.raises(Called):
            ProviderAction.update_contact(self.contact, self.provider)

    def test_update_right_record(self, default_database):
        contact2 = ProviderContact(
            provider=self.provider,
            kind=ContactKind.phone,
            value='+483254794'
        )
        default_database.add(contact2)

        update_action = action_factory(ContactUpdate)

        new_value = '+9685749821'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert default_database.query(ProviderContact).count() == 2
        _, ok = update_action(self.contact, self.provider)
        assert ok
        assert default_database.query(ProviderContact).count() == 2

        updated_contact = default_database.query(ProviderContact).filter(
            ProviderContact.id == self.contact.id,
            ProviderContact.value == new_value
        )
        assert updated_contact.count() == 1

        stay_contact = default_database.query(ProviderContact).filter(
            ProviderContact.id == contact2.id,
            ProviderContact.value == contact2.value
        )
        assert stay_contact.count() == 1
