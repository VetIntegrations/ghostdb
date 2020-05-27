from datetime import datetime, timedelta

from ghostdb.db.models.tests import factories
from .. import revenue
from ...kpi import KPISelector


class TestPMSGrossRevenueTransations:

    def test_process(self, dbsession, monkeypatch):
        log = []

        def filter_successful_transactions(order_rel, query):
            log.append('filter_successful_transactions')
            return query

        monkeypatch.setattr(revenue, 'filter_successful_transactions', filter_successful_transactions)

        selector = revenue.PMSGrossRevenueTransations(dbsession, None, KPISelector(dbsession))
        assert not len(log)
        records, status = selector()
        assert log == [
            'filter_successful_transactions',
        ]

    def test_with_all_filters(self, dbsession, monkeypatch):
        log = []

        def filter_successful_transactions(order_rel, query):
            log.append('filter_successful_transactions')
            return query

        def filter_orderitem_by_timerange(query, datetime_from, datetime_to):
            log.append(('filter_transation_timerange', datetime_from, datetime_to))
            return query

        def filter_orderitem_by_corporation(order_rel, query, corp):
            log.append(('filter_transation_corporation', corp))
            return query

        selectorset = KPISelector(dbsession)
        monkeypatch.setattr(revenue, 'filter_successful_transactions', filter_successful_transactions)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_corporation', filter_orderitem_by_corporation)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_timerange', filter_orderitem_by_timerange)

        selector = revenue.PMSGrossRevenueTransations(dbsession, None, selectorset)
        assert not len(log)
        corporation = factories.CorporationFactory()
        dt_from = datetime.now().date()
        dt_to = datetime.now().date() + timedelta(days=1)
        records, status = selector.with_all_filters(corporation, dt_from, dt_to)
        assert log == [
            'filter_successful_transactions',
            ('filter_transation_corporation', corporation),
            ('filter_transation_timerange', dt_from, dt_to),
        ]
