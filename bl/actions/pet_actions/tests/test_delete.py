import pytest

from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit
from ghostdb.bl.actions.utils.base import action_factory
from ..delete import (
    PetDelete, BreedDelete, ColorDelete, GenderDelete, SpeciesDelete,
    WeightUnitDelete
)


class TestPetDelete:

    @pytest.fixture(autouse=True)
    def setup_pet(self, default_database):
        self.pet = Pet(name='Ricky')
        default_database.add(self.pet)

    def test_ok(self, default_database):
        delete_action = action_factory(PetDelete)

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

        monkeypatch.setattr(PetDelete, 'process', process)

        with pytest.raises(Called):
            PetAction.delete(self.pet)

    def test_delete_right_record(self, default_database):
        pet = Pet(name='Buch')
        default_database.add(pet)

        delete_action = action_factory(PetDelete)

        assert default_database.query(Pet).count() == 2
        _, ok = delete_action(self.pet)
        assert ok
        assert default_database.query(Pet).count() == 1

        assert default_database.query(Pet)[0] == pet


class TestBreedDelete:

    @pytest.fixture(autouse=True)
    def setup_breed(self, default_database):
        self.breed = Breed(name='Beagle')
        default_database.add(self.breed)

    def test_ok(self, default_database):
        delete_action = action_factory(BreedDelete)

        assert default_database.query(Breed).count() == 1
        _, ok = delete_action(self.breed)
        assert ok
        assert default_database.query(Breed).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import BreedAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedDelete, 'process', process)

        with pytest.raises(Called):
            BreedAction.delete(self.breed)

    def test_delete_right_record(self, default_database):
        breed = Breed(name='American Staffordshire Terrier')
        default_database.add(breed)

        delete_action = action_factory(BreedDelete)

        assert default_database.query(Breed).count() == 2
        _, ok = delete_action(self.breed)
        assert ok
        assert default_database.query(Breed).count() == 1

        assert default_database.query(Breed)[0] == breed


class TestColorDelete:

    @pytest.fixture(autouse=True)
    def setup_color(self, default_database):
        self.color = Color(name='Black')
        default_database.add(self.color)

    def test_ok(self, default_database):
        delete_action = action_factory(ColorDelete)

        assert default_database.query(Color).count() == 1
        _, ok = delete_action(self.color)
        assert ok
        assert default_database.query(Color).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import ColorAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorDelete, 'process', process)

        with pytest.raises(Called):
            ColorAction.delete(self.color)

    def test_delete_right_record(self, default_database):
        color = Color(name='Red')
        default_database.add(color)

        delete_action = action_factory(ColorDelete)

        assert default_database.query(Color).count() == 2
        _, ok = delete_action(self.color)
        assert ok
        assert default_database.query(Color).count() == 1

        assert default_database.query(Color)[0] == color


class TestGenderDelete:

    @pytest.fixture(autouse=True)
    def setup_gender(self, default_database):
        self.gender = Gender(name='female')
        default_database.add(self.gender)

    def test_ok(self, default_database):
        delete_action = action_factory(GenderDelete)

        assert default_database.query(Gender).count() == 1
        _, ok = delete_action(self.gender)
        assert ok
        assert default_database.query(Gender).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import GenderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderDelete, 'process', process)

        with pytest.raises(Called):
            GenderAction.delete(self.gender)

    def test_delete_right_record(self, default_database):
        gender = Gender(name='male')
        default_database.add(gender)

        delete_action = action_factory(GenderDelete)

        assert default_database.query(Gender).count() == 2
        _, ok = delete_action(self.gender)
        assert ok
        assert default_database.query(Gender).count() == 1

        assert default_database.query(Gender)[0] == gender


class TestSpeciesDelete:

    @pytest.fixture(autouse=True)
    def setup_species(self, default_database):
        self.species = Species(name='Canine')
        default_database.add(self.species)

    def test_ok(self, default_database):
        delete_action = action_factory(SpeciesDelete)

        assert default_database.query(Species).count() == 1
        _, ok = delete_action(self.species)
        assert ok
        assert default_database.query(Species).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import SpeciesAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesDelete, 'process', process)

        with pytest.raises(Called):
            SpeciesAction.delete(self.species)

    def test_delete_right_record(self, default_database):
        species = Species(name='Fenine')
        default_database.add(species)

        delete_action = action_factory(SpeciesDelete)

        assert default_database.query(Species).count() == 2
        _, ok = delete_action(self.species)
        assert ok
        assert default_database.query(Species).count() == 1

        assert default_database.query(Species)[0] == species


class TestWeightUnitDelete:

    @pytest.fixture(autouse=True)
    def setup_weight_unit(self, default_database):
        self.weight_unit = WeightUnit(name='kg')
        default_database.add(self.weight_unit)

    def test_ok(self, default_database):
        delete_action = action_factory(WeightUnitDelete)

        assert default_database.query(WeightUnit).count() == 1
        _, ok = delete_action(self.weight_unit)
        assert ok
        assert default_database.query(WeightUnit).count() == 0

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import WeightUnitAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitDelete, 'process', process)

        with pytest.raises(Called):
            WeightUnitAction.delete(self.weight_unit)

    def test_delete_right_record(self, default_database):
        unit = WeightUnit(name='Fenine')
        default_database.add(unit)

        delete_action = action_factory(WeightUnitDelete)

        assert default_database.query(WeightUnit).count() == 2
        _, ok = delete_action(self.weight_unit)
        assert ok
        assert default_database.query(WeightUnit).count() == 1

        assert default_database.query(WeightUnit)[0] == unit
