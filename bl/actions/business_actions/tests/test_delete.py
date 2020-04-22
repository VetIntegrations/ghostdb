import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business, BusinessContact, ContactKind
from ghostdb.bl.actions.business import BusinessAction
from ..delete import BusinessDelete, ContactDelete


class TestBusinessDelete:

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

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Business).count() == 1
        _, ok = BusinessAction(dbsession).delete(self.business)
        assert ok
        assert dbsession.query(Business).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BusinessDelete, 'process', process)

        with pytest.raises(Called):
            BusinessAction(dbsession).delete(self.business)

    def test_delete_right_record(self, dbsession, event_off):
        business2 = Business(
            corporation=self.corp,
            name='Wet Nose',
            display_name='Wet Nose'
        )
        dbsession.add(business2)

        assert dbsession.query(Business).count() == 2
        _, ok = BusinessAction(dbsession).delete(self.business)
        assert ok
        assert dbsession.query(Business).count() == 1

        assert dbsession.query(Business)[0] == business2


class TestBusinessContactDelete:

    @pytest.fixture(autouse=True)
    def setup_contact(self, dbsession):
        self.corp = Corporation(name='Test Corporation 1')
        self.business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        self.contact = BusinessContact(
            business=self.business,
            kind=ContactKind.email,
            value='aah@testcorp1.local'
        )
        dbsession.add(self.corp)
        dbsession.add(self.business)
        dbsession.add(self.contact)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(BusinessContact).count() == 1
        _, ok = BusinessAction(dbsession).remove_contact(self.contact, self.business)
        assert ok
        assert dbsession.query(BusinessContact).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactDelete, 'process', process)

        with pytest.raises(Called):
            BusinessAction(dbsession).remove_contact(self.contact, self.business)

    def test_delete_right_record(self, dbsession, event_off):
        contact2 = BusinessContact(
            business=self.business,
            kind=ContactKind.phone,
            value='+47532895983274'
        )
        dbsession.add(contact2)

        assert dbsession.query(BusinessContact).count() == 2
        _, ok = BusinessAction(dbsession).remove_contact(self.contact, self.business)
        assert ok
        assert dbsession.query(BusinessContact).count() == 1

        assert dbsession.query(BusinessContact)[0] == contact2
