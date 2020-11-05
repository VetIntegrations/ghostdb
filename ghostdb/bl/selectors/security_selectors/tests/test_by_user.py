import pytest
from datetime import datetime, timedelta

from ghostdb.db.models.security import TemporaryToken
from ghostdb.db.models.tests.factories import UserFactory
from ..by_user import TemporatyTokenActiveByUser


class TestTemporaryTokenActiveByUserUtc:

    @pytest.fixture(autouse=True)
    def setup_user(self):
        self.user = UserFactory()

    def test_token_by_user_ok(self, dbsession):
        token = TemporaryToken(
            token='123',
            user_id=self.user.id,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        dbsession.add(token)
        selector = TemporatyTokenActiveByUser(dbsession, TemporaryToken, None)
        tokens_query = selector(self.user.id)
        assert tokens_query.first() == token

    def test_expired_not_ok(self, dbsession):
        token = TemporaryToken(
            token='123',
            user_id=self.user.id,
            expires_at=datetime.utcnow()
        )
        dbsession.add(token)
        selector = TemporatyTokenActiveByUser(dbsession, TemporaryToken, None)
        tokens_query = selector(self.user.id)
        assert tokens_query.count() == 0

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.security import TemporaryTokenSelector

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(TemporatyTokenActiveByUser, 'process', process)

        with pytest.raises(Called):
            TemporaryTokenSelector(dbsession).active_by_user()
