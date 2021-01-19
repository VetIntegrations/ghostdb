import pytest
from datetime import datetime, timedelta

from ghostdb.db.models.tests.factories import UserFactory, TemporaryTokenFactory
from ghostdb.db.models.user import User
from ghostdb.bl.selectors.user import UserSelector
from ghostdb.db.models.security import TokenKind
from ..by_not_verification_email import FindNotVerificationUsers


class TestFindNotVerificationUsers:

    def test_filtering(self, dbsession):
        user_1 = UserFactory(is_ghost=True)
        user_2 = UserFactory(is_ghost=True)
        user_3 = UserFactory(is_ghost=True)
        user_4 = UserFactory(is_ghost=False)

        # user_1 has expired token
        TemporaryTokenFactory(
            user=user_1,
            kind=TokenKind.EMAIL_VALIDATION,
            expires_at=datetime.utcnow() - timedelta(minutes=5)
        )

        # user_2 doesn't have any tokens

        # user_3 has active token
        TemporaryTokenFactory(
            user=user_3,
            kind=TokenKind.EMAIL_VALIDATION,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )

        # user_4 also has expired token but he is active user
        TemporaryTokenFactory(user=user_4, expires_at=datetime.utcnow() - timedelta(minutes=5))

        assert dbsession.query(User).count() == 4
        query = UserSelector(dbsession).by_not_verification_email()
        assert query.count() == 2
        assert sorted(query.all(), key=lambda x: x.id) == [user_1, user_2, ]

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        user = User(email='test@localhost', deleted=None)
        dbsession.add(user)

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(FindNotVerificationUsers, 'process', process)

        with pytest.raises(Called):
            UserSelector(dbsession).by_not_verification_email()
