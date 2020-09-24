import pytest

from ghostdb.db.models.security import TemporaryToken
from ghostdb.bl.actions.security import TemporaryTokenAction
from ..create import TemporaryTokenCreate


class TestTeporaryTokenCreate:

    def test_ok(self, dbsession, event_off):
        token = TemporaryToken(token='123')

        assert dbsession.query(TemporaryToken).count() == 0
        action = TemporaryTokenAction(dbsession, event_bus=None, customer_name='VIS')
        new_token, ok = action.create(token)
        assert ok
        assert new_token == token
        assert dbsession.query(TemporaryToken).count() == 1
        event_off.assert_called_once()

    def test_prefill_token_value(self, dbsession, event_off):
        token = TemporaryToken()

        assert dbsession.query(TemporaryToken).count() == 0
        action = TemporaryTokenAction(dbsession, event_bus=None, customer_name='VIS')
        new_token, ok = action.create(token)
        assert ok
        assert new_token == token
        assert new_token.token
        assert dbsession.query(TemporaryToken).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(TemporaryTokenCreate, 'process', process)

        token = TemporaryToken()
        action = TemporaryTokenAction(dbsession, event_bus=None, customer_name='VIS')
        with pytest.raises(Called):
            action.create(token)
