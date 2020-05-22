from datetime import datetime, timedelta

from ghostdb.db.models.tests import factories
from .. import discount


class TestPMSDiscountedTransations:

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

        monkeypatch.setattr(discount, 'filter_successful_transactions', filter_successful_transactions)
        monkeypatch.setattr(discount, 'filter_transation_timerange', filter_transation_timerange)
        monkeypatch.setattr(discount, 'filter_transation_corporation', filter_transation_corporation)

        selector = discount.PMSDiscountedTransations(dbsession, None)
        assert not len(log)
        dt_from = datetime.now().date()
        dt_to = datetime.now().date() + timedelta(days=1)
        records, status = selector(corporation, dt_from, dt_to)
        assert log == [
            ('filter_transation_corporation', corporation),
            'filter_successful_transactions',
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

        selector = discount.PMSDiscountedTransations(dbsession, None)
        records, status = selector(
            order.corporation, datetime.now().date(), datetime.now().date() + timedelta(days=1)
        )
        assert records.count() == 1
        assert records[0].unit_price == 5
