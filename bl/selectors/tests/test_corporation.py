import uuid
import pytest

from ghostdb.db.models.corporation import Corporation


class TestByID:

    @pytest.fixture(autouse=True)
    def corporation(self, default_database):
        self.corp = Corporation(name='Test Corporation')
        default_database.add(self.corp)
        default_database.commit()

    def test_ok(self, default_database):
        from ..corporation import CorporationSelector

        corp, ok = CorporationSelector.by_id(self.corp.id)

        assert ok
        assert corp == self.corp

    def test_not_found(self, default_database):
        from ..corporation import CorporationSelector

        corp, ok = CorporationSelector.by_id(uuid.uuid4())

        assert not ok
        assert corp is None
