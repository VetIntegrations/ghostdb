import pytest
from datetime import datetime, timedelta

from ghostdb.db.models import user as user_models
from ghostdb.db.models.security import TemporaryToken
from ..by_user import TemporaryTokenByUserUtc


class TestTemporaryTokenByUserUtc:

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = user_models.User(first_name='Jon', email='test@localhost.com')
        dbsession.add(self.user)
        dbsession.commit()

    def test_token_by_user_ok(self, dbsession):
        token = TemporaryToken(
            token='123',
            user_id = self.user.id,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        dbsession.add(token)
        selector = TemporaryTokenByUserUtc(dbsession, TemporaryToken, None)
        token_from_db, ok = selector(self.user.id)
        assert ok
        assert token_from_db == token

    def test_expired_not_ok(self, dbsession):
        token = TemporaryToken(
            token='123',
            user_id = self.user.id,
            expires_at=datetime.utcnow()
        )
        dbsession.add(token)
        selector = TemporaryTokenByUserUtc(dbsession, TemporaryToken, None)
        token_from_db, ok = selector(self.user.id)
        assert not ok
        assert token_from_db is None
