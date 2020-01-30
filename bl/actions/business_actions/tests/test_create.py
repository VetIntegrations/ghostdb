import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business, BusinessContact, ContactKind
from ghostdb.bl.actions.utils.base import action_factory
from ..create import BusinessCreate, ContactCreate


class TestBusinessCreate:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, default_database):
        self.corp = Corporation(name='Test Corporation 1')
        default_database.add(self.corp)
        default_database.commit()

    def test_ok(self, default_database):
        create_action = action_factory(BusinessCreate)

        business = Business(
            corporation_id=self.corp.id,
            name='Antlers and Hooves',
            display_name='Antlers and Hooves'
        )

        assert default_database.query(Business).count() == 0
        new_business, ok = create_action(business)
        assert ok
        assert new_business == business
        assert default_database.query(Business).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.business import BusinessAction

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
        with pytest.raises(Called):
            BusinessAction.create(business)


class TestBusinessContactCreate:

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
        default_database.commit()

    def test_ok(self, default_database):
        create_action = action_factory(ContactCreate)

        contact = BusinessContact(
            business_id=self.business.id,
            kind=ContactKind.email,
            value='aah@tcorp.local'
        )

        assert default_database.query(BusinessContact).count() == 0
        new_contact, ok = create_action(contact, self.business)
        assert ok
        assert new_contact == contact
        assert default_database.query(BusinessContact).count() == 1

    def test_prefill_business(self, default_database):
        create_action = action_factory(ContactCreate)

        contact = BusinessContact(
            kind=ContactKind.email,
            value='aah@tcorp.local'
        )

        assert default_database.query(BusinessContact).count() == 0
        new_contact, ok = create_action(contact, self.business)
        assert ok
        assert new_contact == contact
        assert new_contact.business_id == self.business.id
        assert default_database.query(BusinessContact).count() == 1
        query_business_contact = (
            default_database
            .query(BusinessContact)
            .filter(BusinessContact.business == self.business)
        )
        assert query_business_contact.count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.business import BusinessAction

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
        with pytest.raises(Called):
            BusinessAction.add_contact(contact, self.business)
