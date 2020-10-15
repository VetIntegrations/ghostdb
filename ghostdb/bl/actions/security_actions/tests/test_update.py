import pytest
from datetime import datetime

from ghostdb.db.models.security import TemporaryToken
from ghostdb.db.models.tests.factories import TemporaryTokenFactory
from ghostdb.bl.actions.security import TemporaryTokenAction
from ..update import TemporaryTokenUpdate


class TestTemporaryTokenUpdate:

    @pytest.fixture(autouse=True)
    def setup_token(self, dbsession):
        self.token = TemporaryTokenFactory()
        dbsession.add(self.token)

    def test_ok(self, dbsession, event_off):
        new_expires_at = datetime(2020, 1, 1, 18, 26)
        assert new_expires_at != self.token.expires_at

        self.token.expires_at = new_expires_at

        assert dbsession.query(TemporaryToken).count() == 1
        action = TemporaryTokenAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        token, ok = action.update(self.token)
        assert ok
        assert token == self.token
        assert dbsession.query(TemporaryToken).count() == 1
        event_off.assert_called_once()

        updated_token = dbsession.query(TemporaryToken)[0]
        assert updated_token.token == self.token.token
        assert updated_token.expires_at == new_expires_at

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(TemporaryTokenUpdate, 'process', process)

        action = TemporaryTokenAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.token)

    def test_update_right_record(self, dbsession, event_off):
        token = TemporaryTokenFactory()
        dbsession.add(token)

        new_expires_at = datetime(2020, 1, 1, 18, 26)
        assert new_expires_at != self.token.expires_at

        self.token.expires_at = new_expires_at

        assert dbsession.query(TemporaryToken).count() == 2
        action = TemporaryTokenAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.token)
        assert ok
        assert dbsession.query(TemporaryToken).count() == 2

        updated_token = dbsession.query(TemporaryToken).filter(
            TemporaryToken.token == self.token.token,
            TemporaryToken.expires_at == new_expires_at
        )
        assert updated_token.count() == 1

        stay_token = dbsession.query(TemporaryToken).filter(
            TemporaryToken.token == token.token,
            TemporaryToken.expires_at == token.expires_at
        )
        assert stay_token.count() == 1
