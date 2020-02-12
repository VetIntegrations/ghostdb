import pytest

from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit
from ghostdb.bl.actions.pet import (
    PetAction, BreedAction, ColorAction, GenderAction, SpeciesAction,
    WeightUnitAction
)
from ..create import (
    PetCreate, BreedCreate, ColorCreate, GenderCreate, SpeciesCreate,
    WeightUnitCreate
)


class TestPetCreate:

    def test_ok(self, dbsession):
        pet = Pet(name='Ricky')

        assert dbsession.query(Pet).count() == 0
        new_pet, ok = PetAction(dbsession).create(pet)
        assert ok
        assert new_pet == pet
        assert dbsession.query(Pet).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(PetCreate, 'process', process)

        pet = Pet(name='Ricky')
        with pytest.raises(Called):
            PetAction(dbsession).create(pet)


class TestBreedCreate:

    def test_ok(self, dbsession):
        breed = Breed(name='Beagle')

        assert dbsession.query(Breed).count() == 0
        new_breed, ok = BreedAction(dbsession).create(breed)
        assert ok
        assert new_breed == breed
        assert dbsession.query(Breed).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedCreate, 'process', process)

        breed = Breed(name='Beagle')
        with pytest.raises(Called):
            BreedAction(dbsession).create(breed)


class TestColorCreate:

    def test_ok(self, dbsession):
        color = Color(name='Black')

        assert dbsession.query(Color).count() == 0
        new_color, ok = ColorAction(dbsession).create(color)
        assert ok
        assert new_color == color
        assert dbsession.query(Color).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorCreate, 'process', process)

        color = Color(name='Red')
        with pytest.raises(Called):
            ColorAction(dbsession).create(color)


class TestGenderCreate:

    def test_ok(self, dbsession):
        gender = Gender(name='female')

        assert dbsession.query(Gender).count() == 0
        new_gender, ok = GenderAction(dbsession).create(gender)
        assert ok
        assert new_gender == gender
        assert dbsession.query(Gender).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderCreate, 'process', process)

        gender = Gender(name='female')
        with pytest.raises(Called):
            GenderAction(dbsession).create(gender)


class TestSpeciesCreate:

    def test_ok(self, dbsession):
        species = Species(name='Canine')

        assert dbsession.query(Species).count() == 0
        new_species, ok = SpeciesAction(dbsession).create(species)
        assert ok
        assert new_species == species
        assert dbsession.query(Species).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesCreate, 'process', process)

        species = Species(name='Fanine')
        with pytest.raises(Called):
            SpeciesAction(dbsession).create(species)


class TestWeightUnitCreate:

    def test_ok(self, dbsession):
        unit = WeightUnit(name='kg')

        assert dbsession.query(WeightUnit).count() == 0
        new_unit, ok = WeightUnitAction(dbsession).create(unit)
        assert ok
        assert new_unit == unit
        assert dbsession.query(WeightUnit).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitCreate, 'process', process)

        unit = WeightUnit(name='lb')
        with pytest.raises(Called):
            WeightUnitAction(dbsession).create(unit)
