import pytest

from ghostdb.db.models.kpi import KPIValue, KPIKind
from ghostdb.bl.actions.kpi_value import KPIValueAction
from ..update import KPIValueUpdate


class TestKPIValueUpdate:

    @pytest.fixture(autouse=True)
    def setup_kpi(self, dbsession):
        self.kpi = KPIValue(
            kind=KPIKind.FINANCIAL_NET_PROFIT,
            value=95
        )
        dbsession.add(self.kpi)

    def test_ok(self, dbsession, event_off):
        new_value = 85
        assert new_value != self.kpi.value

        self.kpi.value = new_value

        assert dbsession.query(KPIValue).count() == 1
        action = KPIValueAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        kpi, ok = action.update(self.kpi)
        assert ok
        assert kpi == self.kpi
        assert dbsession.query(KPIValue).count() == 1
        event_off.assert_called_once()

        updated_kpi = dbsession.query(KPIValue)[0]
        assert updated_kpi.pk == self.kpi.pk
        assert updated_kpi.value == new_value

    def test_action_class_use_right_action(self, dbsession, monkeypatch):

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(KPIValueUpdate, 'process', process)

        action = KPIValueAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.kpi)

    def test_update_right_record(self, dbsession, event_off):
        kpi2 = KPIValue(
            kind=KPIKind.FINANCIAL_NET_REVENUE,
            value=65
        )
        dbsession.add(kpi2)

        new_value = 85
        assert new_value != self.kpi.value

        self.kpi.value = new_value

        assert dbsession.query(KPIValue).count() == 2
        action = KPIValueAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.kpi)
        assert ok
        assert dbsession.query(KPIValue).count() == 2

        updated_kpi = dbsession.query(KPIValue).filter(
            KPIValue.pk == self.kpi.pk,

            KPIValue.value == new_value
        )
        assert updated_kpi.count() == 1

        stay_kpi = dbsession.query(KPIValue).filter(
            KPIValue.pk == kpi2.pk,
            KPIValue.value == kpi2.value,
            KPIValue.kind == KPIKind.FINANCIAL_NET_REVENUE
        )
        assert stay_kpi.count() == 1
