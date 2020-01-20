import pytest

from ghostdb.db.models.corporation import Corporation
from ..update import Update


class TestCorporationCreate:

    @pytest.fixture(autouse=True)
    def corporation(self, default_database):
        self.corp = Corporation(name='Test Corporation')
        default_database.add(self.corp)

    def test_ok(self, default_database):
        update_action = Update(default_database, [], [])

        new_name = 'John Doe Inc.'
        assert new_name != self.corp.name

        self.corp.name = new_name

        assert default_database.query(Corporation).count() == 1
        corp, ok = update_action(self.corp)
        assert ok
        assert corp == self.corp
        assert default_database.query(Corporation).count() == 1

        updated_corp = default_database.query(Corporation)[0]
        assert updated_corp.id == self.corp.id
        assert updated_corp.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.corporation import CorporationAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Update, 'process', process)

        with pytest.raises(Called):
            CorporationAction.update(self.corp)

    def test_update_right_record(self, default_database):
        corp = Corporation(name='Stay Corp.')
        default_database.add(corp)

        update_action = Update(default_database, [], [])

        new_name = 'John Doe Inc.'
        assert new_name != self.corp.name

        self.corp.name = new_name

        assert default_database.query(Corporation).count() == 2
        _, ok = update_action(self.corp)
        assert ok
        assert default_database.query(Corporation).count() == 2

        updated_corp = default_database.query(Corporation).filter(
            Corporation.id == self.corp.id,
            Corporation.name == new_name
        )
        assert updated_corp.count() == 1

        stay_corp = default_database.query(Corporation).filter(
            Corporation.id == corp.id,
            Corporation.name == corp.name
        )
        assert stay_corp.count() == 1
