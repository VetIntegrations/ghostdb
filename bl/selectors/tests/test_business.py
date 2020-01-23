import uuid
import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business


class TestByID:

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
        from ..business import BusinessSelector

        business, ok = BusinessSelector.by_id(self.business.id)

        assert ok
        assert business.id == self.business.id
        assert business.name == self.business.name
        assert business.display_name == self.business.display_name

    def test_not_found(self, default_database):
        from ..business import BusinessSelector

        business, ok = BusinessSelector.by_id(uuid.uuid4())

        assert not ok
        assert business is None
