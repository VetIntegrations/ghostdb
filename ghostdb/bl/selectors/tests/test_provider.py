import uuid
import pytest

from ghostdb.db.models.provider import Provider, ProviderKind
from ..provider import ProviderSelector, ProviderKindSelector


class TestProviderByID:

    @pytest.fixture(autouse=True)
    def setup_provider(self, dbsession):
        self.provider = Provider(first_name='John', last_name='Doe')
        dbsession.add(self.provider)
        dbsession.commit()

    def test_ok(self, dbsession):
        provider, ok = ProviderSelector(dbsession).by_id(self.provider.id)

        assert ok
        assert provider.id == self.provider.id
        assert provider.first_name == self.provider.first_name
        assert provider.last_name == self.provider.last_name

    def test_not_found(self, dbsession):
        provider, ok = ProviderSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert provider is None


class TestProviderKindByID:

    @pytest.fixture(autouse=True)
    def setup_kind(self, dbsession):
        self.kind = ProviderKind(name='Doctor')
        dbsession.add(self.kind)
        dbsession.commit()

    def test_ok(self, dbsession):
        kind, ok = ProviderKindSelector(dbsession).by_id(self.kind.id)

        assert ok
        assert kind.id == self.kind.id
        assert kind.name == self.kind.name

    def test_not_found(self, dbsession):
        kind, ok = ProviderKindSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert kind is None


class TestProviderKindByIName:

    @pytest.fixture(autouse=True)
    def setup_kind(self, dbsession):
        self.kind = ProviderKind(name='Doctor')
        dbsession.add(self.kind)
        dbsession.commit()

    def test_ok(self, dbsession):
        kind, ok = ProviderKindSelector(dbsession).by_iname(self.kind.name.upper())

        assert ok
        assert kind.id == self.kind.id
        assert kind.name == self.kind.name

    def test_not_found(self, dbsession):
        kind, ok = ProviderKindSelector(dbsession).by_iname('Groomer')

        assert not ok
        assert kind is None
