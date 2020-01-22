import pytest

from ghostdb.db.models.pet import Pet
from ..delete import Delete


class TestPetDelete:

    @pytest.fixture(autouse=True)
    def pet(self, default_database):
        self.pet = Pet(name='Ricky')
        default_database.add(self.pet)

    def test_ok(self, default_database):
        delete_action = Delete(default_database, [], [])

        assert default_database.query(Pet).count() == 1
        _, ok = delete_action(self.pet)
        assert ok
        assert default_database.query(Pet).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import PetAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Delete, 'process', process)

        with pytest.raises(Called):
            PetAction.delete(self.pet)

    def test_delete_right_record(self, default_database):
        pet = Pet(name='Buch')
        default_database.add(pet)

        delete_action = Delete(default_database, [], [])

        assert default_database.query(Pet).count() == 2
        _, ok = delete_action(self.pet)
        assert ok
        assert default_database.query(Pet).count() == 1

        assert default_database.query(Pet)[0] == pet
