import pytest

from ghostdb.db.models.pet import Pet
from ..create import Create


class TestPetCreate:

    def test_ok(self, default_database):
        create_action = Create(default_database, [], [])

        pet = Pet(name='Ricky')

        assert default_database.query(Pet).count() == 0
        new_pet, ok = create_action(pet)
        assert ok
        assert new_pet == pet
        assert default_database.query(Pet).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import PetAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Create, 'process', process)

        pet = Pet(name='Ricky')
        with pytest.raises(Called):
            PetAction.create(pet)
