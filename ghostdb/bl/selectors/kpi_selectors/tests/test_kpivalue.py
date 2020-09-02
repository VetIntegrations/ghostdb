from ghostdb.db.models.tests.factories import (
    CorporationFactory, BusinessFactory, ProviderFactory, InternalKPIValueFactory
)

from ...kpi import InternalKPIValueSelector


class TestInternalKPIValueSelector:

    def test_filter_by_corporation(self, dbsession):
        corp1 = CorporationFactory()
        corp2 = CorporationFactory()

        InternalKPIValueFactory(corporation=corp1)
        kpival2 = InternalKPIValueFactory(corporation=corp2)

        dbsession.flush()

        sel = InternalKPIValueSelector(dbsession)
        query, ok = sel.by_corporation(corp2.id)
        assert ok
        assert query.count() == 1
        assert query[0].id == kpival2.id

    def test_filter_by_business(self, dbsession):
        corp = CorporationFactory()
        business1 = BusinessFactory(corporation=corp)
        business2 = BusinessFactory(corporation=corp)

        InternalKPIValueFactory(corporation=corp, business=business1)
        kpival2 = InternalKPIValueFactory(corporation=corp, business=business2)

        dbsession.flush()

        sel = InternalKPIValueSelector(dbsession)
        query, ok = sel.by_business(business2.id)
        assert ok
        assert query.count() == 1
        assert query[0].id == kpival2.id

    def test_filter_by_provider(self, dbsession):
        corp = CorporationFactory()
        business = BusinessFactory(corporation=corp)
        provider1 = ProviderFactory(business=business)
        provider2 = ProviderFactory(business=business)

        InternalKPIValueFactory(corporation=corp, provider=provider1)
        kpival2 = InternalKPIValueFactory(corporation=corp, provider=provider2)

        dbsession.flush()

        sel = InternalKPIValueSelector(dbsession)
        query, ok = sel.by_provider(provider2.id)
        assert ok
        assert query.count() == 1
        assert query[0].id == kpival2.id
