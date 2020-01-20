import pytest

from ghostdb.db.models.corporation import Corporation
from ..by_id import ByID


class TestCorporationSelectByID:

    @pytest.fixture(autouse=True)
    def corporation(self, default_database):
        self.corp = Corporation(name='Test Corporation')
        default_database.add(self.corp)

    def test_ok(self, default_database):
        selector = ByID(default_database, Corporation)

        assert default_database.query(Corporation).count() == 1
        corp, ok = selector(self.corp.id)
        assert ok
        assert corp == self.corp

    def test_selector_class_use_right_selector(self, default_database, monkeypatch):
        from ghostdb.bl.selectors.corporation import CorporationSelector

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ByID, 'process', process)

        with pytest.raises(Called):
            CorporationSelector.by_id(self.corp.id)

    def test_get_right_record(self, default_database):
        new_corp = Corporation(name='Test Corporation 2')
        default_database.add(new_corp)

        selector = ByID(default_database, Corporation)

        assert default_database.query(Corporation).count() == 2
        corp, ok = selector(self.corp.id)
        assert ok
        assert corp == self.corp
