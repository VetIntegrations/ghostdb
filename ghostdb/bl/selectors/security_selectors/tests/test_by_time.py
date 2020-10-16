import pytest
from datetime import date, datetime, timedelta

from ghostdb.db.models.security import TemporaryToken, TokenKind
from ghostdb.db.models.tests.factories import TemporaryTokenFactory
from ..by_time import TemporaryTokenExpired, TemporaryTokenFilterByExpireDate


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


class TestFilterByExpireDate:

    def test_filtering(self, dbsession):
        token = TemporaryTokenFactory(
            kind=TokenKind.CORPORATION_INVITE,
            expires_at=datetime(2020, 5, 15, 3, 54)
        )
        TemporaryTokenFactory(
            kind=TokenKind.EMAIL_VALIDATION,
            expires_at=datetime(2020, 5, 15, 3, 54)
        )
        TemporaryTokenFactory(
            kind=TokenKind.CORPORATION_INVITE,
            expires_at=datetime(2020, 5, 14, 3, 54)
        )
        TemporaryTokenFactory(
            kind=TokenKind.CORPORATION_INVITE,
            expires_at=datetime(2020, 5, 16, 3, 54)
        )

        selector = TemporaryTokenFilterByExpireDate(dbsession, TemporaryToken, None)

        assert dbsession.query(TemporaryToken).count() == 4
        query = selector(date(2020, 5, 15), kind=TokenKind.CORPORATION_INVITE)
        assert query.count() == 1
        assert query.all() == [token]

    def test_filtering_without_kind(self, dbsession):
        token1 = TemporaryTokenFactory(
            kind=TokenKind.CORPORATION_INVITE,
            expires_at=datetime(2020, 5, 15, 3, 54)
        )
        token2 = TemporaryTokenFactory(
            kind=TokenKind.EMAIL_VALIDATION,
            expires_at=datetime(2020, 5, 15, 3, 54)
        )
        TemporaryTokenFactory(
            kind=TokenKind.CORPORATION_INVITE,
            expires_at=datetime(2020, 5, 14, 3, 54)
        )
        TemporaryTokenFactory(
            kind=TokenKind.CORPORATION_INVITE,
            expires_at=datetime(2020, 5, 16, 3, 54)
        )

        selector = TemporaryTokenFilterByExpireDate(dbsession, TemporaryToken, None)

        assert dbsession.query(TemporaryToken).count() == 4
        query = selector(date(2020, 5, 15))
        assert query.count() == 2
        assert query.all() == [token1, token2]

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.security import TemporaryTokenSelector

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(TemporaryTokenFilterByExpireDate, 'process', process)

        with pytest.raises(Called):
            TemporaryTokenSelector(dbsession).filter_by_expire_date()
