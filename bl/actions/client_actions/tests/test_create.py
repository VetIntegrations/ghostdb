import pytest

from ghostdb.db.models.client import Client
from ..create import Create


class TestClientCreate:

    def test_ok(self, default_database):
        create_action = Create(default_database, [], [])

        client = Client(first_name='John', last_name='Doe')

        assert default_database.query(Client).count() == 0
        new_client, ok = create_action(client)
        assert ok
        assert new_client == client
        assert default_database.query(Client).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Create, 'process', process)

        client = Client(first_name='John', last_name='Doe')
        with pytest.raises(Called):
            ClientAction.create(client)
