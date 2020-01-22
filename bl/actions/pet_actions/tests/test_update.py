import pytest

from ghostdb.db.models.pet import Pet
from ..update import Update


class TestPetUpdate:

    @pytest.fixture(autouse=True)
    def pet(self, default_database):
        self.pet = Pet(name='Ricky')
        default_database.add(self.pet)

    def test_ok(self, default_database):
        update_action = Update(default_database, [], [])

        new_name = 'Rocky'
        assert new_name != self.pet.name

        self.pet.name = new_name

        assert default_database.query(Pet).count() == 1
        pet, ok = update_action(self.pet)
        assert ok
        assert pet == self.pet
        assert default_database.query(Pet).count() == 1

        updated_pet = default_database.query(Pet)[0]
        assert updated_pet.id == self.pet.id
        assert updated_pet.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import PetAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Update, 'process', process)

        with pytest.raises(Called):
            PetAction.update(self.pet)

    def test_update_right_record(self, default_database):
        pet2 = Pet(name='Buch')
        default_database.add(pet2)

        update_action = Update(default_database, [], [])

        new_name = 'Rocky'
        assert new_name != self.pet.name

        self.pet.name = new_name

        assert default_database.query(Pet).count() == 2
        _, ok = update_action(self.pet)
        assert ok
        assert default_database.query(Pet).count() == 2

        updated_pet = default_database.query(Pet).filter(
            Pet.id == self.pet.id,
            Pet.name == new_name
        )
        assert updated_pet.count() == 1

        stay_pet = default_database.query(Pet).filter(
            Pet.id == pet2.id,
            Pet.name == pet2.name
        )
        assert stay_pet.count() == 1
