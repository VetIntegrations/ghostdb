import uuid

from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.tests.factories import CorporationFactory
from ..generic import ByID


class TestByID:

    def test_get_one_record(self, dbsession, event_off):
        corp1 = CorporationFactory()
        CorporationFactory()

        result, ok = ByID(dbsession, Corporation, None)(corp1.id)
        assert ok
        assert result == corp1

    def test_not_found_one_record(self, dbsession, event_off):
        CorporationFactory()

        result, ok = ByID(dbsession, Corporation, None)(uuid.uuid1())
        assert not ok
        assert result is None

    def test_get_set_of_records(self, dbsession, event_off):
        corp1 = CorporationFactory()
        CorporationFactory()
        corp3 = CorporationFactory()

        result, ok = ByID(dbsession, Corporation, None)((corp1.id, corp3.id))
        assert ok
        assert result.all() == [corp1, corp3]

    def test_not_found_set_of_records(self, dbsession, event_off):
        CorporationFactory()
        CorporationFactory()

        result, ok = ByID(dbsession, Corporation, None)((uuid.uuid1(), uuid.uuid1()))
        assert ok
        assert not result.all()

    def test_get_set_of_records_without_one(self, dbsession, event_off):
        corp1 = CorporationFactory()
        CorporationFactory()

        result, ok = ByID(dbsession, Corporation, None)((corp1.id, uuid.uuid1()))
        assert ok
        assert result.all() == [corp1]
