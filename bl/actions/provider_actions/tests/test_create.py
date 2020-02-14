import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ContactKind, ProviderKind
from ghostdb.bl.actions.provider import ProviderAction, ProviderKindAction
from ..create import ProviderCreate, ContactCreate, ProviderKindCreate


class TestProviderCreate:

    def test_ok(self, dbsession):
        provider = Provider(first_name='John', last_name='Doe')

        assert dbsession.query(Provider).count() == 0
        new_provider, ok = ProviderAction(dbsession).create(provider)
        assert ok
        assert new_provider == provider
        assert dbsession.query(Provider).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderCreate, 'process', process)

        provider = Provider(first_name='John', last_name='Doe')
        with pytest.raises(Called):
            ProviderAction(dbsession).create(provider)


class TestProviderContactCreate:

    @pytest.fixture(autouse=True)
    def setup_provider(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        dbsession.add(self.provider)
        dbsession.commit()

    def test_ok(self, dbsession):
        contact = ProviderContact(
            provider_id=self.provider.id,
            kind=ContactKind.phone,
            value='+4783294432'
        )

        assert dbsession.query(ProviderContact).count() == 0
        new_contact, ok = ProviderAction(dbsession).add_contact(contact, self.provider)
        assert ok
        assert new_contact == contact
        assert dbsession.query(ProviderContact).count() == 1

    def test_prefill_provider(self, dbsession):
        contact = ProviderContact(
            kind=ContactKind.phone,
            value='+487329478932'
        )

        assert dbsession.query(ProviderContact).count() == 0
        new_contact, ok = ProviderAction(dbsession).add_contact(contact, self.provider)
        assert ok
        assert new_contact == contact
        assert new_contact.provider_id == self.provider.id
        assert dbsession.query(ProviderContact).count() == 1
        query_provider_contact = (
            dbsession
            .query(ProviderContact)
            .filter(ProviderContact.provider == self.provider)
        )
        assert query_provider_contact.count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
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
            ProviderAction(dbsession).add_contact(contact, self.provider)


class TestProviderKindCreate:

    def test_ok(self, dbsession):
        kind = ProviderKind(name='Doctor')

        assert dbsession.query(ProviderKind).count() == 0
        new_kind, ok = ProviderKindAction(dbsession).create(kind)
        assert ok
        assert new_kind == kind
        assert dbsession.query(ProviderKind).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderKindCreate, 'process', process)

        kind = ProviderKind(name='Doctor')
        with pytest.raises(Called):
            ProviderKindAction(dbsession).create(kind)
