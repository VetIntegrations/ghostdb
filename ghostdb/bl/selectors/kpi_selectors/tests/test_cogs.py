from datetime import datetime, timedelta

from unittest.mock import Mock

from ghostdb.db.models.tests import factories
from .. import cogs
from ...kpi import KPISelector


class TestPMSCOGSTransations:

    def test_process(self, dbsession, monkeypatch):
        mock_process = Mock()
        monkeypatch.setattr(cogs.PMSCOGSTransations, 'process', mock_process)

        selector = cogs.PMSCOGSTransations(dbsession, None, None)
        selector()
        assert mock_process.called

    def test_payments_with_all_filters(self, dbsession, monkeypatch):
        log = []

        def filter_payments_by_timerange(query, datetime_from, datetime_to):
            log.append(('filter_payments_by_timerange', datetime_from, datetime_to))
            return query

        def filter_payments_by_business(query, corp):
            log.append(('filter_payments_by_business', corp))
            return query

        selectorset = KPISelector(dbsession)
        monkeypatch.setattr(selectorset, 'filter_payments_by_timerange', filter_payments_by_timerange)
        monkeypatch.setattr(selectorset, 'filter_payments_by_business', filter_payments_by_business)

        selector = cogs.PMSCOGSTransations(dbsession, None, selectorset)
        assert not len(log)
        business = factories.BusinessFactory()
        dt_from = datetime.now().date()
        dt_to = datetime.now().date() + timedelta(days=1)
        records, status = selector.payments_with_all_filters(business, dt_from, dt_to)
        assert log == [
            ('filter_payments_by_business', business),
            ('filter_payments_by_timerange', dt_from, dt_to),
        ]
