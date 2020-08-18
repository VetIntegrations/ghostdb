import pytest

from ghostdb.db.models.provider import Provider, ProviderContact, ProviderContactKind, ProviderKind
from ghostdb.bl.actions.provider import ProviderAction, ProviderKindAction
from ..update import ProviderUpdate, ContactUpdate, ProviderKindUpdate


class TestProviderUpdate:

    @pytest.fixture(autouse=True)
    def setup_provider(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        dbsession.add(self.provider)

    def test_ok(self, dbsession, event_off):
        new_last_name = 'Krispi'
        assert new_last_name != self.provider.last_name

        self.provider.last_name = new_last_name

        assert dbsession.query(Provider).count() == 1
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        provider, ok = action.update(self.provider)
        assert ok
        assert provider == self.provider
        assert dbsession.query(Provider).count() == 1
        event_off.assert_called_once()

        updated_provider = dbsession.query(Provider)[0]
        assert updated_provider.id == self.provider.id
        assert updated_provider.last_name == new_last_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderUpdate, 'process', process)

        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.provider)

    def test_update_right_record(self, dbsession, event_off):
        provider2 = Provider(first_name='Jane', last_name='Doe')
        dbsession.add(provider2)

        new_last_name = 'Ktulhu'
        assert new_last_name != self.provider.last_name

        self.provider.last_name = new_last_name

        assert dbsession.query(Provider).count() == 2
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.provider)
        assert ok
        assert dbsession.query(Provider).count() == 2

        updated_provider = dbsession.query(Provider).filter(
            Provider.id == self.provider.id,
            Provider.last_name == new_last_name
        )
        assert updated_provider.count() == 1

        stay_provider = dbsession.query(Provider).filter(
            Provider.id == provider2.id,
            Provider.last_name == provider2.last_name
        )
        assert stay_provider.count() == 1


class TestProviderContactUpdate:

    @pytest.fixture(autouse=True)
    def setup_contact(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        self.contact = ProviderContact(
            provider=self.provider,
            kind=ProviderContactKind.phone,
            value='+5874923'
        )
        dbsession.add(self.provider)
        dbsession.add(self.contact)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        new_value = '+473829473'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert dbsession.query(ProviderContact).count() == 1
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        contact, ok = action.update_contact(self.contact, self.provider)
        assert ok
        assert contact == self.contact
        assert dbsession.query(ProviderContact).count() == 1
        event_off.assert_called_once()

        updated_contact = dbsession.query(ProviderContact)[0]
        assert updated_contact.id == self.contact.id
        assert updated_contact.value == new_value

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactUpdate, 'process', process)

        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update_contact(self.contact, self.provider)

    def test_update_right_record(self, dbsession, event_off):
        contact2 = ProviderContact(
            provider=self.provider,
            kind=ProviderContactKind.phone,
            value='+483254794'
        )
        dbsession.add(contact2)

        new_value = '+9685749821'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert dbsession.query(ProviderContact).count() == 2
        action = ProviderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update_contact(self.contact, self.provider)
        assert ok
        assert dbsession.query(ProviderContact).count() == 2

        updated_contact = dbsession.query(ProviderContact).filter(
            ProviderContact.id == self.contact.id,
            ProviderContact.value == new_value
        )
        assert updated_contact.count() == 1

        stay_contact = dbsession.query(ProviderContact).filter(
            ProviderContact.id == contact2.id,
            ProviderContact.value == contact2.value
        )
        assert stay_contact.count() == 1


class TestProviderKindUpdate:

    @pytest.fixture(autouse=True)
    def setup_kind(self, dbsession):
        self.kind = ProviderKind(name='Doctor')
        dbsession.add(self.kind)

    def test_ok(self, dbsession, event_off):
        new_name = 'Groomer'
        assert new_name != self.kind.name

        self.kind.name = new_name

        assert dbsession.query(ProviderKind).count() == 1
        action = ProviderKindAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        kind, ok = action.update(self.kind)
        assert ok
        assert kind == self.kind
        assert dbsession.query(ProviderKind).count() == 1
        event_off.assert_called_once()

        updated_kind = dbsession.query(ProviderKind)[0]
        assert updated_kind.id == self.kind.id
        assert updated_kind.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ProviderKindUpdate, 'process', process)

        action = ProviderKindAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.kind)

    def test_update_right_record(self, dbsession, event_off):
        kind2 = ProviderKind(name='Masseur')
        dbsession.add(kind2)

        new_name = 'Groomer'
        assert new_name != self.kind.name

        self.kind.name = new_name

        assert dbsession.query(ProviderKind).count() == 2
        action = ProviderKindAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.kind)
        assert ok
        assert dbsession.query(ProviderKind).count() == 2

        updated_kind = dbsession.query(ProviderKind).filter(
            ProviderKind.id == self.kind.id,
            ProviderKind.name == new_name
        )
        assert updated_kind.count() == 1

        stay_kind = dbsession.query(ProviderKind).filter(
            ProviderKind.id == kind2.id,
            ProviderKind.name == kind2.name
        )
        assert stay_kind.count() == 1
