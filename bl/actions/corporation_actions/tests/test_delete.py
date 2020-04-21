import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.bl.actions.corporation import CorporationAction
from ..delete import Delete


class TestCorporationDelete:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation')
        dbsession.add(self.corp)

    def test_ok(self, dbsession):
        assert dbsession.query(Corporation).count() == 1
        _, ok = CorporationAction(dbsession).delete(self.corp)
        assert ok
        assert dbsession.query(Corporation).count() == 0

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Delete, 'process', process)

        with pytest.raises(Called):
            CorporationAction(dbsession).delete(self.corp)

    def test_delete_right_record(self, dbsession):
        corp = Corporation(name='Test Corporation Stay')
        dbsession.add(corp)

        assert dbsession.query(Corporation).count() == 2
        _, ok = CorporationAction(dbsession).delete(self.corp)
        assert ok
        assert dbsession.query(Corporation).count() == 1

        assert dbsession.query(Corporation)[0] == corp
