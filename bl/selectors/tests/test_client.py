import uuid
import pytest

from ghostdb.db.models.client import Client


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_client(self, default_database):
        self.client = Client(first_name='John', last_name='Doe')
        default_database.add(self.client)
        default_database.commit()

    def test_ok(self, default_database):
        from ..client import ClientSelector

        client, ok = ClientSelector(default_database).by_id(self.client.id)

        assert ok
        assert client.id == self.client.id
        assert client.first_name == self.client.first_name
        assert client.last_name == self.client.last_name

    def test_not_found(self, default_database):
        from ..client import ClientSelector

        client, ok = ClientSelector(default_database).by_id(uuid.uuid4())

        assert not ok
        assert client is None
