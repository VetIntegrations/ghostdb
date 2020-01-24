import uuid
import pytest

from ghostdb.db.models.pet import Pet


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_pet(self, default_database):
        self.pet = Pet(name='Ricky')
        default_database.add(self.pet)
        default_database.commit()

    def test_ok(self, default_database):
        from ..pet import PetSelector

        pet, ok = PetSelector.by_id(self.pet.id)

        assert ok
        assert pet.id == self.pet.id
        assert pet.name == self.pet.name

    def test_not_found(self, default_database):
        from ..pet import PetSelector

        pet, ok = PetSelector.by_id(uuid.uuid4())

        assert not ok
        assert pet is None
