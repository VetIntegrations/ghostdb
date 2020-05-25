import pytest

from ghostdb.db.models.kpi import KPIValue, KPIKind
from ghostdb.bl.actions.kpi_value import KPIValueAction
from ..create import KPIValueCreate


class TestKPIValueCreate:

    def test_ok(self, dbsession, event_off):
        kpi = KPIValue(
            kind=KPIKind.FINANCIAL_NET_PROFIT,
            value=95
        )

        assert dbsession.query(KPIValue).count() == 0
        new_kpi, ok = KPIValueAction(dbsession).create(kpi)
        assert ok
        assert new_kpi == kpi
        assert dbsession.query(KPIValue).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(KPIValueCreate, 'process', process)

        kpi = KPIValue(
            kind=KPIKind.FINANCIAL_NET_PROFIT,
            value=95
        )
        with pytest.raises(Called):
            KPIValueAction(dbsession).create(kpi)