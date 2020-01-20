import pytest

from ghostdb.db.models.corporation import Corporation
from ..create import Create


class TestCorporationCreate:

    def test_ok(self, default_database):
        create_action = Create(default_database, [], [])

        corp = Corporation(name='Test Corp 1')

        assert default_database.query(Corporation).count() == 0
        new_corp, ok = create_action(corp)
        assert ok
        assert new_corp == corp
        assert default_database.query(Corporation).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.corporation import CorporationAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Create, 'process', process)

        corp = Corporation(name='Test Corp 1')
        with pytest.raises(Called):
            CorporationAction.create(corp)
