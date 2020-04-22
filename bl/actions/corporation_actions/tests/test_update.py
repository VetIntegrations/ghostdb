import pytest

from ghostdb.db.models.corporation import Corporation
from ghostdb.bl.actions.corporation import CorporationAction
from ..update import Update


class TestCorporationUpdate:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation')
        dbsession.add(self.corp)

    def test_ok(self, dbsession, event_off):
        new_name = 'John Doe Inc.'
        assert new_name != self.corp.name

        self.corp.name = new_name

        assert dbsession.query(Corporation).count() == 1
        corp, ok = CorporationAction(dbsession).update(self.corp)
        assert ok
        assert corp == self.corp
        assert dbsession.query(Corporation).count() == 1
        event_off.assert_called_once()

        updated_corp = dbsession.query(Corporation)[0]
        assert updated_corp.id == self.corp.id
        assert updated_corp.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Update, 'process', process)

        with pytest.raises(Called):
            CorporationAction(dbsession).update(self.corp)

    def test_update_right_record(self, dbsession, event_off):
        corp = Corporation(name='Stay Corp.')
        dbsession.add(corp)

        new_name = 'John Doe Inc.'
        assert new_name != self.corp.name

        self.corp.name = new_name

        assert dbsession.query(Corporation).count() == 2
        _, ok = CorporationAction(dbsession).update(self.corp)
        assert ok
        assert dbsession.query(Corporation).count() == 2

        updated_corp = dbsession.query(Corporation).filter(
            Corporation.id == self.corp.id,
            Corporation.name == new_name
        )
        assert updated_corp.count() == 1

        stay_corp = dbsession.query(Corporation).filter(
            Corporation.id == corp.id,
            Corporation.name == corp.name
        )
        assert stay_corp.count() == 1
