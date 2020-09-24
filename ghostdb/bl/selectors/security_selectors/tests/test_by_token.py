import pytest
from datetime import datetime, timedelta

from ghostdb.db.models.security import TemporaryToken
from ..by_token import TemporaryTokenByTokenUtc


class TestTemporaryTokenByTokenUtc:

    def test_ok(self, dbsession):
        token = TemporaryToken(
            token='123',
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        dbsession.add(token)

        selector = TemporaryTokenByTokenUtc(dbsession, TemporaryToken, None)

        assert dbsession.query(TemporaryToken).count() == 1
        token_from_db, ok = selector(token.token)
        assert ok
        assert token_from_db == token

    def test_expired(self, dbsession):
        token = TemporaryToken(
            token='123',
            expires_at=datetime.utcnow()
        )
        dbsession.add(token)

        selector = TemporaryTokenByTokenUtc(dbsession, TemporaryToken, None)

        assert dbsession.query(TemporaryToken).filter(TemporaryToken.token == token.token).count() == 1
        token_from_db, ok = selector(token.token)
        assert not ok
        assert token_from_db is None

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.security import TemporaryTokenSelector

        token = TemporaryToken(
            token='123',
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        dbsession.add(token)

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(TemporaryTokenByTokenUtc, 'process', process)

        with pytest.raises(Called):
            TemporaryTokenSelector(dbsession).by_token_utc(token.token)
