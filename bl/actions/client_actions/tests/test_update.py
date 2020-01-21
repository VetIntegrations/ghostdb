import pytest

from ghostdb.db.models.client import Client
from ..update import Update


class TestClientUpdate:

    @pytest.fixture(autouse=True)
    def client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)

    def test_ok(self, default_database):
        update_action = Update(default_database, [], [])

        new_last_name = 'Krispi'
        assert new_last_name != self.client.last_name

        self.client.last_name = new_last_name

        assert default_database.query(Client).count() == 1
        client, ok = update_action(self.client)
        assert ok
        assert client == self.client
        assert default_database.query(Client).count() == 1

        updated_client = default_database.query(Client)[0]
        assert updated_client.id == self.client.id
        assert updated_client.last_name == new_last_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.client import ClientAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Update, 'process', process)

        with pytest.raises(Called):
            ClientAction.update(self.client)

    def test_update_right_record(self, default_database):
        client = Client(first_name='Jane', last_name='Doe')
        default_database.add(client)

        update_action = Update(default_database, [], [])

        new_last_name = 'Ktulhu'
        assert new_last_name != self.client.last_name

        self.client.last_name = new_last_name

        assert default_database.query(Client).count() == 2
        _, ok = update_action(self.client)
        assert ok
        assert default_database.query(Client).count() == 2

        updated_client = default_database.query(Client).filter(
            Client.id == self.client.id,
            Client.last_name == new_last_name
        )
        assert updated_client.count() == 1

        stay_client = default_database.query(Client).filter(
            Client.id == client.id,
            Client.last_name == client.last_name
        )
        assert stay_client.count() == 1
