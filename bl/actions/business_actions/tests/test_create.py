import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business, BusinessContact, ContactKind
from ghostdb.bl.actions.business import BusinessAction
from ..create import BusinessCreate, ContactCreate


class TestBusinessCreate:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation 1')
        dbsession.add(self.corp)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        business = Business(
            corporation_id=self.corp.id,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )

        assert dbsession.query(Business).count() == 0
        action = BusinessAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_business, ok = action.create(business)
        assert ok
        assert new_business == business
        assert dbsession.query(Business).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch, event_off):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BusinessCreate, 'process', process)

        business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        action = BusinessAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(business)


class TestBusinessContactCreate:

    @pytest.fixture(autouse=True)
    def setup_business(self, dbsession):
        self.corp = Corporation(name='Test Corporation 1')
        self.business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        dbsession.add(self.corp)
        dbsession.add(self.business)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        contact = BusinessContact(
            business_id=self.business.id,
            kind=ContactKind.email,
            value='aah@tcorp.local'
        )

        assert dbsession.query(BusinessContact).count() == 0
        action = BusinessAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_contact, ok = action.add_contact(contact, self.business)
        assert ok
        assert new_contact == contact
        assert dbsession.query(BusinessContact).count() == 1
        event_off.assert_called_once()

    def test_prefill_business(self, dbsession, event_off):
        contact = BusinessContact(
            kind=ContactKind.email,
            value='aah@tcorp.local'
        )

        assert dbsession.query(BusinessContact).count() == 0
        action = BusinessAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_contact, ok = action.add_contact(contact, self.business)
        assert ok
        assert new_contact == contact
        assert new_contact.business_id == self.business.id
        assert dbsession.query(BusinessContact).count() == 1
        query_business_contact = (
            dbsession
            .query(BusinessContact)
            .filter(BusinessContact.business == self.business)
        )
        assert query_business_contact.count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactCreate, 'process', process)

        contact = BusinessContact(
            business_id=self.business.id,
            kind=ContactKind.email,
            value='aah@tcorp.local'
        )
        action = BusinessAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_contact(contact, self.business)
