import uuid
import pytest

from ghostdb.db.models.corporation import Corporation
from ..corporation import CorporationSelector


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation')
        dbsession.add(self.corp)
        dbsession.commit()

    def test_ok(self, dbsession):
        corp, ok = CorporationSelector(dbsession).by_id(self.corp.id)

        assert ok
        assert corp == self.corp

    def test_not_found(self, dbsession):
        corp, ok = CorporationSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert corp is None
