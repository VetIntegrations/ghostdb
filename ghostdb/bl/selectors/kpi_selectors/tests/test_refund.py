from datetime import datetime, timedelta

from ghostdb.db.models.tests import factories
from .. import refund
from ...kpi import KPISelector


class TestPMSRefundTransations:

    def test_process(self, dbsession, monkeypatch):
        log = []

        def filter_successful_transactions(order_rel, query):
            log.append('filter_successful_transactions')
            return query

        monkeypatch.setattr(refund, 'filter_successful_transactions', filter_successful_transactions)

        selector = refund.PMSRefundTransactions(dbsession, None, None)
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
        monkeypatch.setattr(refund, 'filter_successful_transactions', filter_successful_transactions)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_corporation', filter_orderitem_by_corporation)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_timerange', filter_orderitem_by_timerange)

        selector = refund.PMSRefundTransactions(dbsession, None, selectorset)
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

    def test_filter_by_description(self, dbsession):
        order = factories.OrderFactory()
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=2, amount=-300, description='it is refund transaction'
        )
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=3, amount=-300, description='Refund'
        )
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=4, amount=-300, description='Refunded'
        )

        # shouldn't be in a list
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=5, amount=-300, description='Sell of goods'
        )

        selector = refund.PMSRefundTransactions(dbsession, None, None)
        records, status = selector()

        assert records.count() == 3
        assert 5 not in [record.unit_price for record in records]

    def test_filter_by_amount(self, dbsession):
        order = factories.OrderFactory()
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=2, amount=-300, description='Refund'
        )
        # shouldn't be in a list
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=3, amount=300, description='Refund'
        )
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=4, amount=0, description='Refund'
        )

        selector = refund.PMSRefundTransactions(dbsession, None, None)
        records, status = selector()

        assert records.count() == 1
        assert records[0].unit_price == 2
