import pytest

from ghostdb.db.models.user import User
from ..getting import ByEmail


class TestByEmail:

    def test_ok(self, dbsession):
        user = User(email='test@localhost')
        user2 = User(email='test2@localhost')
        dbsession.add(user)
        dbsession.add(user2)

        selector = ByEmail(dbsession, User, None)

        assert dbsession.query(User).count() == 2
        user_from_db, ok = selector(user.email)
        assert ok
        assert user_from_db == user

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.user import UserSelector

        user = User(email='test@localhost')
        dbsession.add(user)

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ByEmail, 'process', process)

        with pytest.raises(Called):
            UserSelector(dbsession).by_email(user.email)
