import pytest

from ghostdb.db.models.user import User
from ghostdb.bl.actions.user import UserAction
from ..update import UserUpdate


class TestUserUpdate:

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = User(email='test@localhost')
        dbsession.add(self.user)

    def test_ok(self, dbsession, event_off):
        new_email = 'test@example'
        assert new_email != self.user.email

        self.user.email = new_email

        assert dbsession.query(User).count() == 1
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        user, ok = action.update(self.user)
        assert ok
        assert user == self.user
        assert dbsession.query(User).count() == 1
        event_off.assert_called_once()

        updated_user = dbsession.query(User)[0]
        assert updated_user.id == self.user.id
        assert updated_user.email == new_email

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(UserUpdate, 'process', process)

        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.user)

    def test_update_right_record(self, dbsession, event_off):
        user = User(email='test@vet')
        dbsession.add(user)

        new_email = 'text@dev'
        assert new_email != self.user.email

        self.user.email = new_email

        assert dbsession.query(User).count() == 2
        action = UserAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.user)
        assert ok
        assert dbsession.query(User).count() == 2

        updated_user = dbsession.query(User).filter(
            User.id == self.user.id,
            User.email == new_email
        )
        assert updated_user.count() == 1

        stay_user = dbsession.query(User).filter(
            User.id == user.id,
            User.email == user.email
        )
        assert stay_user.count() == 1
