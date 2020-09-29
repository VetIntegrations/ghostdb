import pytest
import sqlalchemy.exc

from ghostdb.db.models.user import User
from ghostdb.bl.actions.user import UserAction
from ..create import UserCreate


class TestUserCreate:

    def test_ok(self, dbsession, event_off):
        user = User(email='test@localhost')

        assert dbsession.query(User).count() == 0
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_user, ok = action.create(user)
        assert ok
        assert new_user == user
        assert dbsession.query(User).count() == 1
        event_off.assert_called_once()

    def test_email_unique(self, dbsession, event_off):
        existing_user = User(email='test@localhost')
        dbsession.add(existing_user)

        user = User(email='test@localhost')

        assert dbsession.query(User).count() == 1
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            new_user, ok = action.create(user)

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(UserCreate, 'process', process)

        user = User(email='test@localhost')
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(user)
