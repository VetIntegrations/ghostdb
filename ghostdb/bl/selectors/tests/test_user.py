import uuid
import pytest

from ghostdb.db.models import user as user_models
from .. import user as user_selectors


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = user_models.User(first_name='Jon')
        dbsession.add(self.user)
        dbsession.commit()

    def test_ok(self, dbsession):
        user, ok = user_selectors.UserSelector(dbsession).by_id(self.user.id)

        assert ok
        assert user.id == self.user.id
        assert user.first_name == self.user.first_name

    def test_not_found(self, dbsession):
        user, ok = user_selectors.UserSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert user is None
