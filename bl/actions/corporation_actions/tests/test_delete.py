import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.bl.actions.utils.base import action_factory
from ..delete import Delete


class TestCorporationDelete:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, default_database):
        self.corp = Corporation(name='Test Corporation')
        default_database.add(self.corp)

    def test_ok(self, default_database):
        delete_action = action_factory(Delete)

        assert default_database.query(Corporation).count() == 1
        _, ok = delete_action(self.corp)
        assert ok
        assert default_database.query(Corporation).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.corporation import CorporationAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Delete, 'process', process)

        with pytest.raises(Called):
            CorporationAction.delete(self.corp)

    def test_delete_right_record(self, default_database):
        corp = Corporation(name='Test Corporation Stay')
        default_database.add(corp)

        delete_action = action_factory(Delete)

        assert default_database.query(Corporation).count() == 2
        _, ok = delete_action(self.corp)
        assert ok
        assert default_database.query(Corporation).count() == 1

        assert default_database.query(Corporation)[0] == corp
