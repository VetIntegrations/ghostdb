import pytest
from datetime import datetime, timedelta

from ghostdb.db.models.tests.factories import UserFactory
from ghostdb.db.models.user import User
from ghostdb.bl.selectors.user import UserSelector
from ..by_deleted import FindDeletedUsers


class TestFindDeletedUsers:

    def test_filtering(self, dbsession):
        UserFactory(deleted=None)
        user_deleted = UserFactory(deleted=datetime.utcnow()-timedelta(minutes=5))

        assert dbsession.query(User).count() == 2
        query = UserSelector(dbsession).by_deleted(datetime.utcnow())
        assert query.count() == 1
        assert query.all() == [user_deleted, ]

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        user = User(email='test@localhost', deleted=None)
        dbsession.add(user)

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(FindDeletedUsers, 'process', process)

        with pytest.raises(Called):
            UserSelector(dbsession).by_deleted(datetime.utcnow())
