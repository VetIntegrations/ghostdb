import uuid
import pytest

from ghostdb.db.models.provider import Provider


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_provider(self, default_database):
        self.provider = Provider(first_name='John', last_name='Doe')
        default_database.add(self.provider)
        default_database.commit()

    def test_ok(self, default_database):
        from ..provider import ProviderSelector

        provider, ok = ProviderSelector.by_id(self.provider.id)

        assert ok
        assert provider.id == self.provider.id
        assert provider.first_name == self.provider.first_name
        assert provider.last_name == self.provider.last_name

    def test_not_found(self, default_database):
        from ..provider import ProviderSelector

        provider, ok = ProviderSelector.by_id(uuid.uuid4())

        assert not ok
        assert provider is None
