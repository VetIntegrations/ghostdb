import pytest

from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit
from ghostdb.bl.actions.pet import (
    PetAction, BreedAction, ColorAction, GenderAction, SpeciesAction,
    WeightUnitAction
)
from ..delete import (
    PetDelete, BreedDelete, ColorDelete, GenderDelete, SpeciesDelete,
    WeightUnitDelete
)


class TestPetDelete:

    @pytest.fixture(autouse=True)
    def setup_pet(self, dbsession):
        self.pet = Pet(name='Ricky')
        dbsession.add(self.pet)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Pet).count() == 1
        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.pet)
        assert ok
        assert dbsession.query(Pet).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        from ghostdb.bl.actions.pet import PetAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(PetDelete, 'process', process)

        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.pet)

    def test_delete_right_record(self, dbsession, event_off):
        pet = Pet(name='Buch')
        dbsession.add(pet)

        assert dbsession.query(Pet).count() == 2
        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.pet)
        assert ok
        assert dbsession.query(Pet).count() == 1

        assert dbsession.query(Pet)[0] == pet


class TestBreedDelete:

    @pytest.fixture(autouse=True)
    def setup_breed(self, dbsession):
        self.breed = Breed(name='Beagle')
        dbsession.add(self.breed)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Breed).count() == 1
        action = BreedAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.breed)
        assert ok
        assert dbsession.query(Breed).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedDelete, 'process', process)

        action = BreedAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.breed)

    def test_delete_right_record(self, dbsession, event_off):
        breed = Breed(name='American Staffordshire Terrier')
        dbsession.add(breed)

        assert dbsession.query(Breed).count() == 2
        action = BreedAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.breed)
        assert ok
        assert dbsession.query(Breed).count() == 1
        event_off.assert_called_once()

        assert dbsession.query(Breed)[0] == breed


class TestColorDelete:

    @pytest.fixture(autouse=True)
    def setup_color(self, dbsession):
        self.color = Color(name='Black')
        dbsession.add(self.color)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Color).count() == 1
        action = ColorAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.color)
        assert ok
        assert dbsession.query(Color).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorDelete, 'process', process)

        action = ColorAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.color)

    def test_delete_right_record(self, dbsession, event_off):
        color = Color(name='Red')
        dbsession.add(color)

        assert dbsession.query(Color).count() == 2
        action = ColorAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.color)
        assert ok
        assert dbsession.query(Color).count() == 1
        event_off.assert_called_once()

        assert dbsession.query(Color)[0] == color


class TestGenderDelete:

    @pytest.fixture(autouse=True)
    def setup_gender(self, dbsession):
        self.gender = Gender(name='female')
        dbsession.add(self.gender)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Gender).count() == 1
        action = GenderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.gender)
        assert ok
        assert dbsession.query(Gender).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderDelete, 'process', process)

        action = GenderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.gender)

    def test_delete_right_record(self, dbsession, event_off):
        gender = Gender(name='male')
        dbsession.add(gender)

        assert dbsession.query(Gender).count() == 2
        action = GenderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.gender)
        assert ok
        assert dbsession.query(Gender).count() == 1
        event_off.assert_called_once()

        assert dbsession.query(Gender)[0] == gender


class TestSpeciesDelete:

    @pytest.fixture(autouse=True)
    def setup_species(self, dbsession):
        self.species = Species(name='Canine')
        dbsession.add(self.species)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Species).count() == 1
        action = SpeciesAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.species)
        assert ok
        assert dbsession.query(Species).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesDelete, 'process', process)

        action = SpeciesAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.species)

    def test_delete_right_record(self, dbsession, event_off):
        species = Species(name='Fenine')
        dbsession.add(species)

        assert dbsession.query(Species).count() == 2
        action = SpeciesAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.species)
        assert ok
        assert dbsession.query(Species).count() == 1

        assert dbsession.query(Species)[0] == species


class TestWeightUnitDelete:

    @pytest.fixture(autouse=True)
    def setup_weight_unit(self, dbsession):
        self.weight_unit = WeightUnit(name='kg')
        dbsession.add(self.weight_unit)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(WeightUnit).count() == 1
        action = WeightUnitAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.weight_unit)
        assert ok
        assert dbsession.query(WeightUnit).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitDelete, 'process', process)

        action = WeightUnitAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.weight_unit)

    def test_delete_right_record(self, dbsession, event_off):
        unit = WeightUnit(name='Fenine')
        dbsession.add(unit)

        assert dbsession.query(WeightUnit).count() == 2
        action = WeightUnitAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.weight_unit)
        assert ok
        assert dbsession.query(WeightUnit).count() == 1

        assert dbsession.query(WeightUnit)[0] == unit
