import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business, BusinessContact, ContactKind
from ..delete import BusinessDelete, ContactDelete


class TestBusinessDelete:

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
        delete_action = BusinessDelete(default_database, [], [])

        assert default_database.query(Business).count() == 1
        _, ok = delete_action(self.business)
        assert ok
        assert default_database.query(Business).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.business import BusinessAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BusinessDelete, 'process', process)

        with pytest.raises(Called):
            BusinessAction.delete(self.business)

    def test_delete_right_record(self, default_database):
        business2 = Business(
            corporation=self.corp,
            name='Wet Nose',
            display_name='Wet Nose'
        )
        default_database.add(business2)

        delete_action = BusinessDelete(default_database, [], [])

        assert default_database.query(Business).count() == 2
        _, ok = delete_action(self.business)
        assert ok
        assert default_database.query(Business).count() == 1

        assert default_database.query(Business)[0] == business2


class TestBusinessContactDelete:

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
        delete_action = ContactDelete(default_database, [], [])

        assert default_database.query(BusinessContact).count() == 1
        _, ok = delete_action(self.business, self.contact)
        assert ok
        assert default_database.query(BusinessContact).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.business import BusinessAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ContactDelete, 'process', process)

        with pytest.raises(Called):
            BusinessAction.remove_contact(self.business, self.contact)

    def test_delete_right_record(self, default_database):
        contact2 = BusinessContact(
            business=self.business,
            kind=ContactKind.phone,
            value='+47532895983274'
        )
        default_database.add(contact2)

        delete_action = ContactDelete(default_database, [], [])

        assert default_database.query(BusinessContact).count() == 2
        _, ok = delete_action(self.business, self.contact)
        assert ok
        assert default_database.query(BusinessContact).count() == 1

        assert default_database.query(BusinessContact)[0] == contact2
