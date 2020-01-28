import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ContactKind
from ..create import ProviderCreate, ContactCreate


class TestProviderCreate:

    def test_ok(self, default_database):
        create_action = ProviderCreate(default_database, [], [])

        provider = Provider(first_name='John', last_name='Doe')

        assert default_database.query(Provider).count() == 0
        new_provider, ok = create_action(provider)
        assert ok
        assert new_provider == provider
        assert default_database.query(Provider).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.provider import ProviderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderCreate, 'process', process)

        provider = Provider(first_name='John', last_name='Doe')
        with pytest.raises(Called):
            ProviderAction.create(provider)


class TestProviderContactCreate:

    @pytest.fixture(autouse=True)
    def setup_provider(self, default_database):
        self.provider = Provider(first_name='John', last_name='Doe')
        default_database.add(self.provider)
        default_database.commit()

    def test_ok(self, default_database):
        create_action = ContactCreate(default_database, [], [])

        contact = ProviderContact(
            provider_id=self.provider.id,
            kind=ContactKind.phone,
            value='+4783294432'
        )

        assert default_database.query(ProviderContact).count() == 0
        new_contact, ok = create_action(self.provider, contact)
        assert ok
        assert new_contact == contact
        assert default_database.query(ProviderContact).count() == 1

    def test_prefill_client(self, default_database):
        create_action = ContactCreate(default_database, [], [])

        contact = ProviderContact(
            kind=ContactKind.phone,
            value='+487329478932'
        )

        assert default_database.query(ProviderContact).count() == 0
        new_contact, ok = create_action(self.provider, contact)
        assert ok
        assert new_contact == contact
        assert new_contact.provider_id == self.provider.id
        assert default_database.query(ProviderContact).count() == 1
        query_provider_contact = (
            default_database
            .query(ProviderContact)
            .filter(ProviderContact.provider == self.provider)
        )
        assert query_provider_contact.count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.provider import ProviderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactCreate, 'process', process)

        contact = ProviderContact(
            provider_id=self.provider.id,
            kind=ContactKind.phone,
            value='+327489327'
        )
        with pytest.raises(Called):
            ProviderAction.add_contact(self.provider, contact)
