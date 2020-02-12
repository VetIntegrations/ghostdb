import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business, BusinessContact, ContactKind
from ghostdb.bl.actions.business import BusinessAction
from ..update import BusinessUpdate, ContactUpdate


class TestBusinessUpdate:

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

    def test_ok(self, dbsession):
        new_name = 'Beaver\'s tail'
        assert new_name != self.business.name

        self.business.name = new_name

        assert dbsession.query(Business).count() == 1
        business, ok = BusinessAction(dbsession).update(self.business)
        assert ok
        assert business == self.business
        assert dbsession.query(Business).count() == 1

        updated_business = dbsession.query(Business)[0]
        assert updated_business.id == self.business.id
        assert updated_business.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BusinessUpdate, 'process', process)

        with pytest.raises(Called):
            BusinessAction(dbsession).update(self.business)

    def test_update_right_record(self, dbsession):
        business2 = Business(
            corporation=self.corp,
            name='Wet Nose',
            display_name='Wet Nose'
        )
        dbsession.add(business2)

        new_name = 'Beaver\'s tail'
        assert new_name != self.business.name

        self.business.name = new_name

        assert dbsession.query(Business).count() == 2
        _, ok = BusinessAction(dbsession).update(self.business)
        assert ok
        assert dbsession.query(Business).count() == 2

        updated_business = dbsession.query(Business).filter(
            Business.id == self.business.id,
            Business.name == new_name
        )
        assert updated_business.count() == 1

        stay_business = dbsession.query(Business).filter(
            Business.id == business2.id,
            Business.name == business2.name
        )
        assert stay_business.count() == 1


class TestBusinessContactUpdate:

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

    def test_ok(self, dbsession):
        new_value = 'hello@aah.local'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert dbsession.query(BusinessContact).count() == 1
        contact, ok = BusinessAction(dbsession).update_contact(self.contact, self.business)
        assert ok
        assert contact == self.contact
        assert dbsession.query(BusinessContact).count() == 1

        updated_contact = dbsession.query(BusinessContact)[0]
        assert updated_contact.id == self.contact.id
        assert updated_contact.value == new_value

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactUpdate, 'process', process)

        with pytest.raises(Called):
            BusinessAction(dbsession).update_contact(self.contact, self.business)

    def test_update_right_record(self, dbsession):
        contact2 = BusinessContact(
            business=self.business,
            kind=ContactKind.phone,
            value='+47532895983274'
        )
        dbsession.add(contact2)

        new_value = 'ping@aah.local'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert dbsession.query(BusinessContact).count() == 2
        _, ok = BusinessAction(dbsession).update_contact(self.contact, self.business)
        assert ok
        assert dbsession.query(BusinessContact).count() == 2

        updated_contact = dbsession.query(BusinessContact).filter(
            BusinessContact.id == self.contact.id,
            BusinessContact.value == new_value
        )
        assert updated_contact.count() == 1

        stay_contact = dbsession.query(BusinessContact).filter(
            BusinessContact.id == contact2.id,
            BusinessContact.value == contact2.value
        )
        assert stay_contact.count() == 1
