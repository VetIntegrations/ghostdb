import pytest
from datetime import datetime

from ghostdb.db.models.user import User
from ghostdb.bl.actions.user import UserAction
from ..update import UserUpdate, MarkAsDeleted, UnmarkAsDeleted


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


class TestMarkUserAsDeleted:

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = User(email='test@localhost')
        dbsession.add(self.user)

    def test_ok(self, dbsession, event_off):

        assert self.user.deleted is None
        assert dbsession.query(User).count() == 1
        action = UserAction(dbsession, None, 'vis')
        user, ok = action.mark_as_deleted(self.user)
        assert ok
        assert user == self.user
        assert dbsession.query(User).count() == 1
        event_off.assert_called_once()

        updated_user = dbsession.query(User)[0]
        assert updated_user.id == self.user.id
        assert updated_user.deleted

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(MarkAsDeleted, 'process', process)

        action = UserAction(dbsession, None, 'vis')
        with pytest.raises(Called):
            action.mark_as_deleted(self.user)

    def test_update_right_record(self, dbsession, event_off):
        new_user = User(email='test@vet')
        dbsession.add(new_user)

        assert self.user.deleted is None
        assert new_user.deleted is None

        assert dbsession.query(User).count() == 2
        action = UserAction(dbsession, None, 'vis')
        _, ok = action.mark_as_deleted(self.user)
        assert ok

        updated_user = dbsession.query(User).filter(
            User.id == self.user.id,
            User.deleted.isnot(None)
        )
        assert updated_user.count() == 1

        stay_user = dbsession.query(User).filter(
            User.id == new_user.id,
            User.deleted.is_(None)
        )
        assert stay_user.count() == 1


class TestUnmarkUserAsDeleted:

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = User(email='test@localhost', deleted=datetime.utcnow())
        dbsession.add(self.user)

    def test_ok(self, dbsession, event_off):

        assert self.user.deleted
        assert dbsession.query(User).count() == 1
        action = UserAction(dbsession, None, 'vis')
        user, ok = action.unmark_as_deleted(self.user)
        assert ok
        assert user == self.user
        assert dbsession.query(User).count() == 1
        event_off.assert_called_once()

        updated_user = dbsession.query(User)[0]
        assert updated_user.id == self.user.id
        assert updated_user.deleted is None

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(UnmarkAsDeleted, 'process', process)

        action = UserAction(dbsession, None, 'vis')
        with pytest.raises(Called):
            action.unmark_as_deleted(self.user)

    def test_update_right_record(self, dbsession, event_off):
        new_user = User(email='test@vet', deleted=datetime.utcnow())
        dbsession.add(new_user)

        assert self.user.deleted
        assert new_user.deleted

        assert dbsession.query(User).count() == 2
        action = UserAction(dbsession, None, 'vis')
        _, ok = action.unmark_as_deleted(self.user)
        assert ok

        updated_user = dbsession.query(User).filter(
            User.id == self.user.id,
            User.deleted.is_(None)
        )
        assert updated_user.count() == 1

        stay_user = dbsession.query(User).filter(
            User.id == new_user.id,
            User.deleted.isnot(None)
        )
        assert stay_user.count() == 1
