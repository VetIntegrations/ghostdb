import pytest

from ghostdb.db.models.client import Client
from ..delete import Delete


class TestClientDelete:

    @pytest.fixture(autouse=True)
    def setup_client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)

    def test_ok(self, default_database):
        delete_action = Delete(default_database, [], [])

        assert default_database.query(Client).count() == 1
        _, ok = delete_action(self.client)
        assert ok
        assert default_database.query(Client).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Delete, 'process', process)

        with pytest.raises(Called):
            ClientAction.delete(self.client)

    def test_delete_right_record(self, default_database):
        client = Client(first_name='Jane', last_name='Doe')
        default_database.add(client)

        delete_action = Delete(default_database, [], [])

        assert default_database.query(Client).count() == 2
        _, ok = delete_action(self.client)
        assert ok
        assert default_database.query(Client).count() == 1

        assert default_database.query(Client)[0] == client
