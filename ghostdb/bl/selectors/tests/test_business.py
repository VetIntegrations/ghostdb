import uuid
import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business
from ..business import BusinessSelector


class TestByID:

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

    def test_ok(self, dbsession):
        business, ok = BusinessSelector(dbsession).by_id(self.business.id)

        assert ok
        assert business.id == self.business.id
        assert business.name == self.business.name
        assert business.display_name == self.business.display_name

    def test_not_found(self, dbsession):
        business, ok = BusinessSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert business is None
