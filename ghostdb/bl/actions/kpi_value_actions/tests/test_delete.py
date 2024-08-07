import pytest

from ghostdb.db.models.kpi import InternalKPIValue, KPIKind
from ghostdb.bl.actions.kpi_value import KPIValueAction
from ..delete import KPIValueDelete


class TestKPIValueDelete:

    @pytest.fixture(autouse=True)
    def setup_kpi(self, dbsession):
        self.kpi = InternalKPIValue(
            kind=KPIKind.FINANCIAL_NET_PROFIT,
            value=95
        )
        dbsession.add(self.kpi)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(InternalKPIValue).count() == 1
        action = KPIValueAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.kpi)
        assert ok
        assert dbsession.query(InternalKPIValue).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(KPIValueDelete, 'process', process)

        action = KPIValueAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.kpi)

    def test_delete_right_record(self, dbsession, event_off):
        kpi2 = InternalKPIValue(
            kind=KPIKind.FINANCIAL_NET_REVENUE,
            value=85
        )
        dbsession.add(kpi2)

        assert dbsession.query(InternalKPIValue).count() == 2
        action = KPIValueAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.kpi)
        assert ok
        assert dbsession.query(InternalKPIValue).count() == 1

        assert dbsession.query(InternalKPIValue)[0] == kpi2
