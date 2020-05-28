import pytest

from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit, PetOwner
from ghostdb.bl.actions.pet import (
    PetAction, BreedAction, ColorAction, GenderAction, SpeciesAction,
    WeightUnitAction
)
from ..create import (
    PetCreate, BreedCreate, ColorCreate, GenderCreate, SpeciesCreate,
    WeightUnitCreate, OwnerCreate
)


class TestPetCreate:

    def test_ok(self, dbsession, event_off):
        pet = Pet(name='Ricky')

        assert dbsession.query(Pet).count() == 0
        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_pet, ok = action.create(pet)
        assert ok
        assert new_pet == pet
        assert dbsession.query(Pet).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(PetCreate, 'process', process)

        pet = Pet(name='Ricky')
        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(pet)


class TestpetOwnerCreate:

    @pytest.fixture(autouse=True)
    def setup(self, dbsession):
        self.pet = Pet(name='Ricky')
        self.client = Client(first_name='John', last_name='Doe')
        dbsession.add(self.client)
        dbsession.add(self.pet)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        owner = PetOwner(
            client_id=self.client.id,
            pet_id=self.pet.id,
            is_primary=False
        )

        assert dbsession.query(PetOwner).count() == 0
        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_owner, ok = action.add_owner(owner)
        assert ok
        assert new_owner == owner
        assert dbsession.query(PetOwner).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OwnerCreate, 'process', process)

        owner = PetOwner(
            client_id=self.client.id,
            pet_id=self.pet.id,
            is_primary=False
        )
        action = PetAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_owner(owner)


class TestBreedCreate:

    def test_ok(self, dbsession, event_off):
        breed = Breed(name='Beagle')

        assert dbsession.query(Breed).count() == 0
        action = BreedAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_breed, ok = action.create(breed)
        assert ok
        assert new_breed == breed
        assert dbsession.query(Breed).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedCreate, 'process', process)

        breed = Breed(name='Beagle')
        action = BreedAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(breed)


class TestColorCreate:

    def test_ok(self, dbsession, event_off):
        color = Color(name='Black')

        assert dbsession.query(Color).count() == 0
        action = ColorAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_color, ok = action.create(color)
        assert ok
        assert new_color == color
        assert dbsession.query(Color).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorCreate, 'process', process)

        color = Color(name='Red')
        action = ColorAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(color)


class TestGenderCreate:

    def test_ok(self, dbsession, event_off):
        gender = Gender(name='female')

        assert dbsession.query(Gender).count() == 0
        action = GenderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_gender, ok = action.create(gender)
        assert ok
        assert new_gender == gender
        assert dbsession.query(Gender).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderCreate, 'process', process)

        gender = Gender(name='female')
        action = GenderAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(gender)


class TestSpeciesCreate:

    def test_ok(self, dbsession, event_off):
        species = Species(name='Canine')

        assert dbsession.query(Species).count() == 0
        action = SpeciesAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_species, ok = action.create(species)
        assert ok
        assert new_species == species
        assert dbsession.query(Species).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesCreate, 'process', process)

        species = Species(name='Fanine')
        action = SpeciesAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(species)


class TestWeightUnitCreate:

    def test_ok(self, dbsession, event_off):
        unit = WeightUnit(name='kg')

        assert dbsession.query(WeightUnit).count() == 0
        action = WeightUnitAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_unit, ok = action.create(unit)
        assert ok
        assert new_unit == unit
        assert dbsession.query(WeightUnit).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitCreate, 'process', process)

        unit = WeightUnit(name='lb')
        action = WeightUnitAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(unit)
