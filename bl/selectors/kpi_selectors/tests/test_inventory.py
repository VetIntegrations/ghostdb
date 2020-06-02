from datetime import datetime, timedelta

from ghostdb.db.models.tests import factories
from .. import inventory
from ...kpi import KPISelector


class TestPMSInventoryTransations:

    def test_use_filters(self, dbsession, monkeypatch):
        log = []

        def filter_successful_transactions(order_rel, query):
            log.append('filter_successful_transactions')
            return query

        monkeypatch.setattr(inventory, 'filter_successful_transactions', filter_successful_transactions)

        selector = inventory.PMSInventoryTransations(dbsession, None, None)
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
        monkeypatch.setattr(inventory, 'filter_successful_transactions', filter_successful_transactions)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_corporation', filter_orderitem_by_corporation)
        monkeypatch.setattr(selectorset, 'filter_orderitem_by_timerange', filter_orderitem_by_timerange)

        selector = inventory.PMSInventoryTransations(dbsession, None, selectorset)
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

    def test_filter_by_inventory(self, dbsession):
        order1 = factories.OrderFactory()
        factories.OrderItemFactory(
            order=order1, quantity=100, unit_price=2, is_inventory=None, created_at=datetime.now()
        )
        inventory_trans1 = factories.OrderItemFactory(
            order=order1, quantity=100, unit_price=5, is_inventory=True, created_at=datetime.now(),
        )
        order2 = factories.OrderFactory()
        factories.OrderItemFactory(
            order=order2, quantity=100, unit_price=7, is_inventory=False, created_at=datetime.now()
        )
        inventory_trans2 = factories.OrderItemFactory(
            order=order2, quantity=100, unit_price=10, is_inventory=True, created_at=datetime.now(),
        )

        selector = inventory.PMSInventoryTransations(dbsession, None, None)
        records, status = selector()
        assert records.count() == 2
        assert set(records.all()) == {inventory_trans1, inventory_trans2}
