import pytest
from datetime import datetime, timedelta

from ghostdb.db.models.security import TemporaryToken
from ..by_time import TemporaryTokenExpired


class TestTemporaryTokenExpired:

    def test_filtering(self, dbsession):
        live_token = TemporaryToken(token='123', expires_at=datetime.utcnow() + timedelta(minutes=10))
        expired_token = TemporaryToken(token='12345', expires_at=datetime.utcnow())
        dbsession.add(live_token)
        dbsession.add(expired_token)

        selector = TemporaryTokenExpired(dbsession, TemporaryToken, None)

        assert dbsession.query(TemporaryToken).count() == 2
        query = selector()
        assert query.count() == 1
        assert query.all() == [expired_token]

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.security import TemporaryTokenSelector

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(TemporaryTokenExpired, 'process', process)

        with pytest.raises(Called):
            TemporaryTokenSelector(dbsession).all_expired()
