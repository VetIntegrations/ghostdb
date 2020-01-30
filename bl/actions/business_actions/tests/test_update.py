import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business, BusinessContact, ContactKind
from ghostdb.bl.actions.utils.base import action_factory
from ..update import BusinessUpdate, ContactUpdate


class TestBusinessUpdate:

    @pytest.fixture(autouse=True)
    def setup_business(self, default_database):
        self.corp = Corporation(name='Test Corporation 1')
        self.business = Business(
            corporation=self.corp,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )
        default_database.add(self.corp)
        default_database.add(self.business)

    def test_ok(self, default_database):
        update_action = action_factory(BusinessUpdate)

        new_name = 'Beaver\'s tail'
        assert new_name != self.business.name

        self.business.name = new_name

        assert default_database.query(Business).count() == 1
        business, ok = update_action(self.business)
        assert ok
        assert business == self.business
        assert default_database.query(Business).count() == 1

        updated_business = default_database.query(Business)[0]
        assert updated_business.id == self.business.id
        assert updated_business.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.business import BusinessAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BusinessUpdate, 'process', process)

        with pytest.raises(Called):
            BusinessAction.update(self.business)

    def test_update_right_record(self, default_database):
        business2 = Business(
            corporation=self.corp,
            name='Wet Nose',
            display_name='Wet Nose'
        )
        default_database.add(business2)

        update_action = action_factory(BusinessUpdate)

        new_name = 'Beaver\'s tail'
        assert new_name != self.business.name

        self.business.name = new_name

        assert default_database.query(Business).count() == 2
        _, ok = update_action(self.business)
        assert ok
        assert default_database.query(Business).count() == 2

        updated_business = default_database.query(Business).filter(
            Business.id == self.business.id,
            Business.name == new_name
        )
        assert updated_business.count() == 1

        stay_business = default_database.query(Business).filter(
            Business.id == business2.id,
            Business.name == business2.name
        )
        assert stay_business.count() == 1


class TestBusinessContactUpdate:

    @pytest.fixture(autouse=True)
    def setup_contact(self, default_database):
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
        default_database.add(self.corp)
        default_database.add(self.business)
        default_database.add(self.contact)

    def test_ok(self, default_database):
        update_action = action_factory(ContactUpdate)

        new_value = 'hello@aah.local'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert default_database.query(BusinessContact).count() == 1
        contact, ok = update_action(self.contact, self.business)
        assert ok
        assert contact == self.contact
        assert default_database.query(BusinessContact).count() == 1

        updated_contact = default_database.query(BusinessContact)[0]
        assert updated_contact.id == self.contact.id
        assert updated_contact.value == new_value

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.business import BusinessAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactUpdate, 'process', process)

        with pytest.raises(Called):
            BusinessAction.update_contact(self.contact, self.business)

    def test_update_right_record(self, default_database):
        contact2 = BusinessContact(
            business=self.business,
            kind=ContactKind.phone,
            value='+47532895983274'
        )
        default_database.add(contact2)

        update_action = action_factory(ContactUpdate)

        new_value = 'ping@aah.local'
        assert new_value != self.contact.value

        self.contact.value = new_value

        assert default_database.query(BusinessContact).count() == 2
        _, ok = update_action(self.contact, self.business)
        assert ok
        assert default_database.query(BusinessContact).count() == 2

        updated_contact = default_database.query(BusinessContact).filter(
            BusinessContact.id == self.contact.id,
            BusinessContact.value == new_value
        )
        assert updated_contact.count() == 1

        stay_contact = default_database.query(BusinessContact).filter(
            BusinessContact.id == contact2.id,
            BusinessContact.value == contact2.value
        )
        assert stay_contact.count() == 1
