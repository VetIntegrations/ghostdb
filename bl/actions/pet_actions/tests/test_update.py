import pytest

from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit
from ghostdb.bl.actions.pet import (
    PetAction, BreedAction, ColorAction, GenderAction, SpeciesAction,
    WeightUnitAction
)
from ..update import (
    PetUpdate, BreedUpdate, ColorUpdate, GenderUpdate, SpeciesUpdate,
    WeightUnitUpdate
)


class TestPetUpdate:

    @pytest.fixture(autouse=True)
    def setup_pet(self, dbsession):
        self.pet = Pet(name='Ricky')
        dbsession.add(self.pet)

    def test_ok(self, dbsession):
        new_name = 'Rocky'
        assert new_name != self.pet.name

        self.pet.name = new_name

        assert dbsession.query(Pet).count() == 1
        pet, ok = PetAction(dbsession).update(self.pet)
        assert ok
        assert pet == self.pet
        assert dbsession.query(Pet).count() == 1

        updated_pet = dbsession.query(Pet)[0]
        assert updated_pet.id == self.pet.id
        assert updated_pet.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        from ghostdb.bl.actions.pet import PetAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(PetUpdate, 'process', process)

        with pytest.raises(Called):
            PetAction(dbsession).update(self.pet)

    def test_update_right_record(self, dbsession):
        pet2 = Pet(name='Buch')
        dbsession.add(pet2)

        new_name = 'Rocky'
        assert new_name != self.pet.name

        self.pet.name = new_name

        assert dbsession.query(Pet).count() == 2
        _, ok = PetAction(dbsession).update(self.pet)
        assert ok
        assert dbsession.query(Pet).count() == 2

        updated_pet = dbsession.query(Pet).filter(
            Pet.id == self.pet.id,

            Pet.name == new_name
        )
        assert updated_pet.count() == 1

        stay_pet = dbsession.query(Pet).filter(
            Pet.id == pet2.id,
            Pet.name == pet2.name
        )
        assert stay_pet.count() == 1


class TestBreedUpdate:

    @pytest.fixture(autouse=True)
    def setup_breed(self, dbsession):
        self.breed = Breed(name='Beable')
        dbsession.add(self.breed)

    def test_ok(self, dbsession):
        new_name = 'American Staffordshire Terrier'
        assert new_name != self.breed.name

        self.breed.name = new_name

        assert dbsession.query(Breed).count() == 1
        breed, ok = BreedAction(dbsession).update(self.breed)
        assert ok
        assert breed == self.breed
        assert dbsession.query(Breed).count() == 1

        updated_breed = dbsession.query(Breed)[0]
        assert updated_breed.id == self.breed.id
        assert updated_breed.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        from ghostdb.bl.actions.pet import BreedAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedUpdate, 'process', process)

        with pytest.raises(Called):
            BreedAction(dbsession).update(self.breed)

    def test_update_right_record(self, dbsession):
        breed2 = Breed(name='American Staffordshire Terrier')
        dbsession.add(breed2)

        new_name = 'Pug'
        assert new_name != self.breed.name

        self.breed.name = new_name

        assert dbsession.query(Breed).count() == 2
        _, ok = BreedAction(dbsession).update(self.breed)
        assert ok
        assert dbsession.query(Breed).count() == 2

        updated_breed = dbsession.query(Breed).filter(
            Breed.id == self.breed.id,
            Breed.name == new_name
        )
        assert updated_breed.count() == 1

        stay_breed = dbsession.query(Breed).filter(
            Breed.id == breed2.id,
            Breed.name == breed2.name
        )
        assert stay_breed.count() == 1


class TestColorUpdate:

    @pytest.fixture(autouse=True)
    def setup_color(self, dbsession):
        self.color = Color(name='Black')
        dbsession.add(self.color)

    def test_ok(self, dbsession):
        new_name = 'Red'
        assert new_name != self.color.name

        self.color.name = new_name

        assert dbsession.query(Color).count() == 1
        color, ok = ColorAction(dbsession).update(self.color)
        assert ok
        assert color == self.color
        assert dbsession.query(Color).count() == 1

        updated_color = dbsession.query(Color)[0]
        assert updated_color.id == self.color.id
        assert updated_color.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorUpdate, 'process', process)

        with pytest.raises(Called):
            ColorAction(dbsession).update(self.color)

    def test_update_right_record(self, dbsession):
        color2 = Color(name='Red')
        dbsession.add(color2)

        new_name = 'White'
        assert new_name != self.color.name

        self.color.name = new_name

        assert dbsession.query(Color).count() == 2
        _, ok = ColorAction(dbsession).update(self.color)
        assert ok
        assert dbsession.query(Color).count() == 2

        updated_color = dbsession.query(Color).filter(
            Color.id == self.color.id,
            Color.name == new_name
        )
        assert updated_color.count() == 1

        stay_color = dbsession.query(Color).filter(
            Color.id == color2.id,
            Color.name == color2.name
        )
        assert stay_color.count() == 1


class TestGenderUpdate:

    @pytest.fixture(autouse=True)
    def setup_gender(self, dbsession):
        self.gender = Gender(name='female')
        dbsession.add(self.gender)

    def test_ok(self, dbsession):
        new_name = 'male'
        assert new_name != self.gender.name

        self.gender.name = new_name

        assert dbsession.query(Gender).count() == 1
        gender, ok = GenderAction(dbsession).update(self.gender)
        assert ok
        assert gender == self.gender
        assert dbsession.query(Gender).count() == 1

        updated_gender = dbsession.query(Gender)[0]
        assert updated_gender.id == self.gender.id
        assert updated_gender.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderUpdate, 'process', process)

        with pytest.raises(Called):
            GenderAction(dbsession).update(self.gender)

    def test_update_right_record(self, dbsession):
        gender2 = Gender(name='male')
        dbsession.add(gender2)

        new_name = 'male neutered'
        assert new_name != self.gender.name

        self.gender.name = new_name

        assert dbsession.query(Gender).count() == 2
        _, ok = GenderAction(dbsession).update(self.gender)
        assert ok
        assert dbsession.query(Gender).count() == 2

        updated_gender = dbsession.query(Gender).filter(
            Gender.id == self.gender.id,
            Gender.name == new_name
        )
        assert updated_gender.count() == 1

        stay_gender = dbsession.query(Gender).filter(
            Gender.id == gender2.id,
            Gender.name == gender2.name
        )
        assert stay_gender.count() == 1


class TestSpeciesUpdate:

    @pytest.fixture(autouse=True)
    def setup_species(self, dbsession):
        self.species = Species(name='Canine')
        dbsession.add(self.species)

    def test_ok(self, dbsession):
        new_name = 'Fenine'
        assert new_name != self.species.name

        self.species.name = new_name

        assert dbsession.query(Species).count() == 1
        species, ok = SpeciesAction(dbsession).update(self.species)
        assert ok
        assert species == self.species
        assert dbsession.query(Species).count() == 1

        updated_species = dbsession.query(Species)[0]
        assert updated_species.id == self.species.id
        assert updated_species.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesUpdate, 'process', process)

        with pytest.raises(Called):
            SpeciesAction(dbsession).update(self.species)

    def test_update_right_record(self, dbsession):
        species2 = Species(name='Fenine')
        dbsession.add(species2)

        new_name = 'Equine'
        assert new_name != self.species.name

        self.species.name = new_name

        assert dbsession.query(Species).count() == 2
        _, ok = SpeciesAction(dbsession).update(self.species)
        assert ok
        assert dbsession.query(Species).count() == 2

        updated_species = dbsession.query(Species).filter(
            Species.id == self.species.id,
            Species.name == new_name
        )
        assert updated_species.count() == 1

        stay_species = dbsession.query(Species).filter(
            Species.id == species2.id,
            Species.name == species2.name
        )
        assert stay_species.count() == 1


class TestWeightUnitUpdate:

    @pytest.fixture(autouse=True)
    def setup_weight_unit(self, dbsession):
        self.weight_unit = WeightUnit(name='kg')
        dbsession.add(self.weight_unit)

    def test_ok(self, dbsession):
        new_name = 'lb'
        assert new_name != self.weight_unit.name

        self.weight_unit.name = new_name

        assert dbsession.query(WeightUnit).count() == 1
        unit, ok = WeightUnitAction(dbsession).update(self.weight_unit)
        assert ok
        assert unit == self.weight_unit
        assert dbsession.query(WeightUnit).count() == 1

        updated_unit = dbsession.query(WeightUnit)[0]
        assert updated_unit.id == self.weight_unit.id
        assert updated_unit.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitUpdate, 'process', process)

        with pytest.raises(Called):
            WeightUnitAction(dbsession).update(self.weight_unit)

    def test_update_right_record(self, dbsession):
        unit2 = WeightUnit(name='lb')
        dbsession.add(unit2)

        new_name = 'kilo'
        assert new_name != self.weight_unit.name

        self.weight_unit.name = new_name

        assert dbsession.query(WeightUnit).count() == 2
        _, ok = WeightUnitAction(dbsession).update(self.weight_unit)
        assert ok
        assert dbsession.query(WeightUnit).count() == 2

        updated_unit = dbsession.query(WeightUnit).filter(
            WeightUnit.id == self.weight_unit.id,
            WeightUnit.name == new_name
        )
        assert updated_unit.count() == 1

        stay_unit = dbsession.query(WeightUnit).filter(
            WeightUnit.id == unit2.id,
            WeightUnit.name == unit2.name
        )
        assert stay_unit.count() == 1
