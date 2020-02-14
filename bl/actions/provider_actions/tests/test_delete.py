import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ContactKind, ProviderKind
from ghostdb.bl.actions.provider import ProviderAction, ProviderKindAction
from ..delete import ProviderDelete, ContactDelete, ProviderKindDelete


class TestProviderDelete:

    @pytest.fixture(autouse=True)
    def setup_provider(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        dbsession.add(self.provider)

    def test_ok(self, dbsession):
        assert dbsession.query(Provider).count() == 1
        _, ok = ProviderAction(dbsession).delete(self.provider)
        assert ok
        assert dbsession.query(Provider).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderDelete, 'process', process)

        with pytest.raises(Called):
            ProviderAction(dbsession).delete(self.provider)

    def test_delete_right_record(self, dbsession):
        provider2 = Provider(first_name='Jane', last_name='Doe')
        dbsession.add(provider2)

        assert dbsession.query(Provider).count() == 2
        _, ok = ProviderAction(dbsession).delete(self.provider)
        assert ok
        assert dbsession.query(Provider).count() == 1

        assert dbsession.query(Provider)[0] == provider2


class TestProviderContactDelete:

    @pytest.fixture(autouse=True)
    def setup_contact(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        self.contact = ProviderContact(
            provider=self.provider,
            kind=ContactKind.phone,
            value='+5874923'
        )
        dbsession.add(self.provider)
        dbsession.add(self.contact)
        dbsession.commit()

    def test_ok(self, dbsession):
        assert dbsession.query(ProviderContact).count() == 1
        _, ok = ProviderAction(dbsession).remove_contact(self.provider, self.contact)
        assert ok
        assert dbsession.query(ProviderContact).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactDelete, 'process', process)

        with pytest.raises(Called):
            ProviderAction(dbsession).remove_contact(self.provider, self.contact)

    def test_delete_right_record(self, dbsession):
        contact2 = ProviderContact(
            provider=self.provider,
            kind=ContactKind.phone,
            value='+48329482739'
        )
        dbsession.add(contact2)

        assert dbsession.query(ProviderContact).count() == 2
        _, ok = ProviderAction(dbsession).remove_contact(self.provider, self.contact)
        assert ok
        assert dbsession.query(ProviderContact).count() == 1

        assert dbsession.query(ProviderContact)[0] == contact2


class TestProviderKindDelete:

    @pytest.fixture(autouse=True)
    def setup_kind(self, dbsession):
        self.kind = ProviderKind(name='Doctor')
        dbsession.add(self.kind)

    def test_ok(self, dbsession):
        assert dbsession.query(ProviderKind).count() == 1
        _, ok = ProviderKindAction(dbsession).delete(self.kind)
        assert ok
        assert dbsession.query(ProviderKind).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderKindDelete, 'process', process)

        with pytest.raises(Called):
            ProviderKindAction(dbsession).delete(self.kind)

    def test_delete_right_record(self, dbsession):
        kind2 = ProviderKind(name='Groomer')
        dbsession.add(kind2)

        assert dbsession.query(ProviderKind).count() == 2
        _, ok = ProviderKindAction(dbsession).delete(self.kind)
        assert ok
        assert dbsession.query(ProviderKind).count() == 1

        assert dbsession.query(ProviderKind)[0] == kind2
