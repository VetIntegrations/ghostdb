import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ContactKind
from ..delete import ProviderDelete, ContactDelete


class TestProviderDelete:

    @pytest.fixture(autouse=True)
    def setup_provider(self, default_database):
        self.provider = Provider(first_name='John', last_name='Doe')
        default_database.add(self.provider)

    def test_ok(self, default_database):
        delete_action = ProviderDelete(default_database, [], [])

        assert default_database.query(Provider).count() == 1
        _, ok = delete_action(self.provider)
        assert ok
        assert default_database.query(Provider).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.provider import ProviderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderDelete, 'process', process)

        with pytest.raises(Called):
            ProviderAction.delete(self.provider)

    def test_delete_right_record(self, default_database):
        provider2 = Provider(first_name='Jane', last_name='Doe')
        default_database.add(provider2)

        delete_action = ProviderDelete(default_database, [], [])

        assert default_database.query(Provider).count() == 2
        _, ok = delete_action(self.provider)
        assert ok
        assert default_database.query(Provider).count() == 1

        assert default_database.query(Provider)[0] == provider2


class TestProviderContactDelete:

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
        delete_action = ContactDelete(default_database, [], [])

        assert default_database.query(ProviderContact).count() == 1
        _, ok = delete_action(self.provider, self.contact)
        assert ok
        assert default_database.query(ProviderContact).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.provider import ProviderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactDelete, 'process', process)

        with pytest.raises(Called):
            ProviderAction.remove_contact(self.provider, self.contact)

    def test_delete_right_record(self, default_database):
        contact2 = ProviderContact(
            provider=self.provider,
            kind=ContactKind.phone,
            value='+48329482739'
        )
        default_database.add(contact2)

        delete_action = ContactDelete(default_database, [], [])

        assert default_database.query(ProviderContact).count() == 2
        _, ok = delete_action(self.provider, self.contact)
        assert ok
        assert default_database.query(ProviderContact).count() == 1

        assert default_database.query(ProviderContact)[0] == contact2
