from datetime import datetime, timedelta

from ghostdb.db.models.tests import factories
from .. import discount
from ...kpi import KPISelector


class TestPMSDiscountedTransations:

    def test_use_filters(self, dbsession, monkeypatch):
        log = []

        def filter_successful_transactions(order_rel, query):
            log.append('filter_successful_transactions')
            return query

        monkeypatch.setattr(discount, 'filter_successful_transactions', filter_successful_transactions)

        selector = discount.PMSDiscountedTransations(dbsession, None, None)
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

        def filter_orderitem_by_business(order_rel, query, corp):
            log.append(('filter_transation_business', corp))
            return query

        selectorset = KPISelector(dbsession)
        monkeypatch.setattr(discount, 'filter_successful_transactions', filter_successful_transactions)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_business', filter_orderitem_by_business)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_timerange', filter_orderitem_by_timerange)

        selector = discount.PMSDiscountedTransations(dbsession, None, selectorset)
        assert not len(log)
        corporation = factories.CorporationFactory()
        dt_from = datetime.now().date()
        dt_to = datetime.now().date() + timedelta(days=1)
        records, status = selector.with_all_filters(corporation, dt_from, dt_to)
        assert log == [
            'filter_successful_transactions',
            ('filter_transation_business', corporation),
            ('filter_transation_timerange', dt_from, dt_to),
        ]

    def test_filter_by_discount_amount(self, dbsession):
        order = factories.OrderFactory()
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=2, discount_amount=None, created_at=datetime.now()
        )
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=5, discount_amount=2, created_at=datetime.now()
        )
        factories.OrderItemFactory(
            order=order, quantity=100, unit_price=7, discount_amount=0, created_at=datetime.now()
        )

        selector = discount.PMSDiscountedTransations(dbsession, None, None)
        records, status = selector()
        assert records.count() == 1
        assert records[0].unit_price == 5
