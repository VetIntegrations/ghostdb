import pytest

from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit
from ghostdb.bl.actions.utils.base import action_factory
from ..create import (
    PetCreate, BreedCreate, ColorCreate, GenderCreate, SpeciesCreate,
    WeightUnitCreate
)


class TestPetCreate:

    def test_ok(self, default_database):
        create_action = action_factory(PetCreate)

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

        monkeypatch.setattr(PetCreate, 'process', process)

        pet = Pet(name='Ricky')
        with pytest.raises(Called):
            PetAction.create(pet)


class TestBreedCreate:

    def test_ok(self, default_database):
        create_action = action_factory(BreedCreate)

        breed = Breed(name='Beagle')

        assert default_database.query(Breed).count() == 0
        new_breed, ok = create_action(breed)
        assert ok
        assert new_breed == breed
        assert default_database.query(Breed).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import BreedAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedCreate, 'process', process)

        breed = Breed(name='Beagle')
        with pytest.raises(Called):
            BreedAction.create(breed)


class TestColorCreate:

    def test_ok(self, default_database):
        create_action = action_factory(ColorCreate)

        color = Color(name='Black')

        assert default_database.query(Color).count() == 0
        new_color, ok = create_action(color)
        assert ok
        assert new_color == color
        assert default_database.query(Color).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import ColorAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorCreate, 'process', process)

        color = Color(name='Red')
        with pytest.raises(Called):
            ColorAction.create(color)


class TestGenderCreate:

    def test_ok(self, default_database):
        create_action = action_factory(GenderCreate)

        gender = Gender(name='female')

        assert default_database.query(Gender).count() == 0
        new_gender, ok = create_action(gender)
        assert ok
        assert new_gender == gender
        assert default_database.query(Gender).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import GenderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderCreate, 'process', process)

        gender = Gender(name='female')
        with pytest.raises(Called):
            GenderAction.create(gender)


class TestSpeciesCreate:

    def test_ok(self, default_database):
        create_action = action_factory(SpeciesCreate)

        species = Species(name='Canine')

        assert default_database.query(Species).count() == 0
        new_species, ok = create_action(species)
        assert ok
        assert new_species == species
        assert default_database.query(Species).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import SpeciesAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesCreate, 'process', process)

        species = Species(name='Fanine')
        with pytest.raises(Called):
            SpeciesAction.create(species)


class TestWeightUnitCreate:

    def test_ok(self, default_database):
        create_action = action_factory(WeightUnitCreate)

        unit = WeightUnit(name='kg')

        assert default_database.query(WeightUnit).count() == 0
        new_unit, ok = create_action(unit)
        assert ok
        assert new_unit == unit
        assert default_database.query(WeightUnit).count() == 1

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import WeightUnitAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitCreate, 'process', process)

        unit = WeightUnit(name='lb')
        with pytest.raises(Called):
            WeightUnitAction.create(unit)
