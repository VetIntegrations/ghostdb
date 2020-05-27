import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ContactKind, ProviderKind
from ghostdb.bl.actions.provider import ProviderAction, ProviderKindAction
from ..create import ProviderCreate, ContactCreate, ProviderKindCreate


class TestProviderCreate:

    def test_ok(self, dbsession, event_off):
        provider = Provider(first_name='John', last_name='Doe')

        assert dbsession.query(Provider).count() == 0
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_provider, ok = action.create(provider)
        assert ok
        assert new_provider == provider
        assert dbsession.query(Provider).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderCreate, 'process', process)

        provider = Provider(first_name='John', last_name='Doe')
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(provider)


class TestProviderContactCreate:

    @pytest.fixture(autouse=True)
    def setup_provider(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        dbsession.add(self.provider)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        contact = ProviderContact(
            provider_id=self.provider.id,
            kind=ContactKind.phone,
            value='+4783294432'
        )

        assert dbsession.query(ProviderContact).count() == 0
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_contact, ok = action.add_contact(contact, self.provider)
        assert ok
        assert new_contact == contact
        assert dbsession.query(ProviderContact).count() == 1
        event_off.assert_called_once()

    def test_prefill_provider(self, dbsession, event_off):
        contact = ProviderContact(
            kind=ContactKind.phone,
            value='+487329478932'
        )

        assert dbsession.query(ProviderContact).count() == 0
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_contact, ok = action.add_contact(contact, self.provider)
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
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_contact(contact, self.provider)


class TestProviderKindCreate:

    def test_ok(self, dbsession, event_off):
        kind = ProviderKind(name='Doctor')

        assert dbsession.query(ProviderKind).count() == 0
        action = ProviderKindAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_kind, ok = action.create(kind)
        assert ok
        assert new_kind == kind
        assert dbsession.query(ProviderKind).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderKindCreate, 'process', process)

        kind = ProviderKind(name='Doctor')
        action = ProviderKindAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(kind)
