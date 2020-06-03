import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.bl.actions.corporation import CorporationAction
from ..create import Create


class TestCorporationCreate:

    def test_ok(self, dbsession, event_off):
        corp = Corporation(name='Test Corp 1')

        assert dbsession.query(Corporation).count() == 0
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_corp, ok = action.create(corp)
        assert ok
        assert new_corp == corp
        assert dbsession.query(Corporation).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Create, 'process', process)

        corp = Corporation(name='Test Corp 1')
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(corp)
