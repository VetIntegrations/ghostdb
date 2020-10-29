import pytest

from ghostdb.db.models.user import User
from ghostdb.bl.actions.user import UserAction
from ..delete import UserDelete


class TestUserDelete:

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = User(email='test@localhost')
        dbsession.add(self.user)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(User).count() == 1
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.user)
        assert ok
        assert dbsession.query(User).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        from ghostdb.bl.actions.user import UserAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(UserDelete, 'process', process)

        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.user)

    def test_delete_right_record(self, dbsession, event_off):
        user = User(email='test2@localhost')
        dbsession.add(user)

        assert dbsession.query(User).count() == 2
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.user)
        assert ok
        assert dbsession.query(User).count() == 1

        assert dbsession.query(User)[0] == user
