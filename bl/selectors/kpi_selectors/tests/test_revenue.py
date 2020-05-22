from datetime import datetime, timedelta

from ghostdb.db.models.tests import factories
from .. import revenue


class TestPMSGrossRevenueTransations:

    def test_use_filters(self, dbsession, monkeypatch):
        log = []
        corporation = factories.CorporationFactory()

        def filter_successful_transactions(order_rel, query):
            log.append('filter_successful_transactions')
            return query

        def filter_transation_timerange(query, datetime_from, datetime_to):
            log.append(('filter_transation_timerange', datetime_from, datetime_to))
            return query

        def filter_transation_corporation(order_rel, query, corp):
            log.append(('filter_transation_corporation', corp))
            return query

        monkeypatch.setattr(revenue, 'filter_successful_transactions', filter_successful_transactions)
        monkeypatch.setattr(revenue, 'filter_transation_timerange', filter_transation_timerange)
        monkeypatch.setattr(revenue, 'filter_transation_corporation', filter_transation_corporation)

        selector = revenue.PMSGrossRevenueTransations(dbsession, None)
        assert not len(log)
        dt_from = datetime.now().date()
        dt_to = datetime.now().date() + timedelta(days=1)
        records, status = selector(corporation, dt_from, dt_to)
        assert log == [
            ('filter_transation_corporation', corporation),
            'filter_successful_transactions',
            ('filter_transation_timerange', dt_from, dt_to),
        ]
