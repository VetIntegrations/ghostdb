import pytest

from ghostdb.db.models.pet import Pet, Breed, Color, Gender, Species, WeightUnit
from ..update import (
    PetUpdate, BreedUpdate, ColorUpdate, GenderUpdate, SpeciesUpdate,
    WeightUnitUpdate
)


class TestPetUpdate:

    @pytest.fixture(autouse=True)
    def setup_pet(self, default_database):
        self.pet = Pet(name='Ricky')
        default_database.add(self.pet)

    def test_ok(self, default_database):
        update_action = PetUpdate(default_database, [], [])

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

        monkeypatch.setattr(PetUpdate, 'process', process)

        with pytest.raises(Called):
            PetAction.update(self.pet)

    def test_update_right_record(self, default_database):
        pet2 = Pet(name='Buch')
        default_database.add(pet2)

        update_action = PetUpdate(default_database, [], [])

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


class TestBreedUpdate:

    @pytest.fixture(autouse=True)
    def setup_breed(self, default_database):
        self.breed = Breed(name='Beable')
        default_database.add(self.breed)

    def test_ok(self, default_database):
        update_action = BreedUpdate(default_database, [], [])

        new_name = 'American Staffordshire Terrier'
        assert new_name != self.breed.name

        self.breed.name = new_name

        assert default_database.query(Breed).count() == 1
        breed, ok = update_action(self.breed)
        assert ok
        assert breed == self.breed
        assert default_database.query(Breed).count() == 1

        updated_breed = default_database.query(Breed)[0]
        assert updated_breed.id == self.breed.id
        assert updated_breed.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import BreedAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(BreedUpdate, 'process', process)

        with pytest.raises(Called):
            BreedAction.update(self.breed)

    def test_update_right_record(self, default_database):
        breed2 = Breed(name='American Staffordshire Terrier')
        default_database.add(breed2)

        update_action = BreedUpdate(default_database, [], [])

        new_name = 'Pug'
        assert new_name != self.breed.name

        self.breed.name = new_name

        assert default_database.query(Breed).count() == 2
        _, ok = update_action(self.breed)
        assert ok
        assert default_database.query(Breed).count() == 2

        updated_breed = default_database.query(Breed).filter(
            Breed.id == self.breed.id,
            Breed.name == new_name
        )
        assert updated_breed.count() == 1

        stay_breed = default_database.query(Breed).filter(
            Breed.id == breed2.id,
            Breed.name == breed2.name
        )
        assert stay_breed.count() == 1


class TestColorUpdate:

    @pytest.fixture(autouse=True)
    def setup_color(self, default_database):
        self.color = Color(name='Black')
        default_database.add(self.color)

    def test_ok(self, default_database):
        update_action = ColorUpdate(default_database, [], [])

        new_name = 'Red'
        assert new_name != self.color.name

        self.color.name = new_name

        assert default_database.query(Color).count() == 1
        color, ok = update_action(self.color)
        assert ok
        assert color == self.color
        assert default_database.query(Color).count() == 1

        updated_color = default_database.query(Color)[0]
        assert updated_color.id == self.color.id
        assert updated_color.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import ColorAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ColorUpdate, 'process', process)

        with pytest.raises(Called):
            ColorAction.update(self.color)

    def test_update_right_record(self, default_database):
        color2 = Color(name='Red')
        default_database.add(color2)

        update_action = ColorUpdate(default_database, [], [])

        new_name = 'White'
        assert new_name != self.color.name

        self.color.name = new_name

        assert default_database.query(Color).count() == 2
        _, ok = update_action(self.color)
        assert ok
        assert default_database.query(Color).count() == 2

        updated_color = default_database.query(Color).filter(
            Color.id == self.color.id,
            Color.name == new_name
        )
        assert updated_color.count() == 1

        stay_color = default_database.query(Color).filter(
            Color.id == color2.id,
            Color.name == color2.name
        )
        assert stay_color.count() == 1


class TestGenderUpdate:

    @pytest.fixture(autouse=True)
    def setup_gender(self, default_database):
        self.gender = Gender(name='female')
        default_database.add(self.gender)

    def test_ok(self, default_database):
        update_action = GenderUpdate(default_database, [], [])

        new_name = 'male'
        assert new_name != self.gender.name

        self.gender.name = new_name

        assert default_database.query(Gender).count() == 1
        gender, ok = update_action(self.gender)
        assert ok
        assert gender == self.gender
        assert default_database.query(Gender).count() == 1

        updated_gender = default_database.query(Gender)[0]
        assert updated_gender.id == self.gender.id
        assert updated_gender.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import GenderAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(GenderUpdate, 'process', process)

        with pytest.raises(Called):
            GenderAction.update(self.gender)

    def test_update_right_record(self, default_database):
        gender2 = Gender(name='male')
        default_database.add(gender2)

        update_action = GenderUpdate(default_database, [], [])

        new_name = 'male neutered'
        assert new_name != self.gender.name

        self.gender.name = new_name

        assert default_database.query(Gender).count() == 2
        _, ok = update_action(self.gender)
        assert ok
        assert default_database.query(Gender).count() == 2

        updated_gender = default_database.query(Gender).filter(
            Gender.id == self.gender.id,
            Gender.name == new_name
        )
        assert updated_gender.count() == 1

        stay_gender = default_database.query(Gender).filter(
            Gender.id == gender2.id,
            Gender.name == gender2.name
        )
        assert stay_gender.count() == 1


class TestSpeciesUpdate:

    @pytest.fixture(autouse=True)
    def setup_species(self, default_database):
        self.species = Species(name='Canine')
        default_database.add(self.species)

    def test_ok(self, default_database):
        update_action = SpeciesUpdate(default_database, [], [])

        new_name = 'Fenine'
        assert new_name != self.species.name

        self.species.name = new_name

        assert default_database.query(Species).count() == 1
        species, ok = update_action(self.species)
        assert ok
        assert species == self.species
        assert default_database.query(Species).count() == 1

        updated_species = default_database.query(Species)[0]
        assert updated_species.id == self.species.id
        assert updated_species.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import SpeciesAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(SpeciesUpdate, 'process', process)

        with pytest.raises(Called):
            SpeciesAction.update(self.species)

    def test_update_right_record(self, default_database):
        species2 = Species(name='Fenine')
        default_database.add(species2)

        update_action = SpeciesUpdate(default_database, [], [])

        new_name = 'Equine'
        assert new_name != self.species.name

        self.species.name = new_name

        assert default_database.query(Species).count() == 2
        _, ok = update_action(self.species)
        assert ok
        assert default_database.query(Species).count() == 2

        updated_species = default_database.query(Species).filter(
            Species.id == self.species.id,
            Species.name == new_name
        )
        assert updated_species.count() == 1

        stay_species = default_database.query(Species).filter(
            Species.id == species2.id,
            Species.name == species2.name
        )
        assert stay_species.count() == 1


class TestWeightUnitUpdate:

    @pytest.fixture(autouse=True)
    def setup_weight_unit(self, default_database):
        self.weight_unit = WeightUnit(name='kg')
        default_database.add(self.weight_unit)

    def test_ok(self, default_database):
        update_action = WeightUnitUpdate(default_database, [], [])

        new_name = 'lb'
        assert new_name != self.weight_unit.name

        self.weight_unit.name = new_name

        assert default_database.query(WeightUnit).count() == 1
        unit, ok = update_action(self.weight_unit)
        assert ok
        assert unit == self.weight_unit
        assert default_database.query(WeightUnit).count() == 1

        updated_unit = default_database.query(WeightUnit)[0]
        assert updated_unit.id == self.weight_unit.id
        assert updated_unit.name == new_name

    def test_action_class_use_right_action(self, default_database, monkeypatch):
        from ghostdb.bl.actions.pet import WeightUnitAction

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WeightUnitUpdate, 'process', process)

        with pytest.raises(Called):
            WeightUnitAction.update(self.weight_unit)

    def test_update_right_record(self, default_database):
        unit2 = WeightUnit(name='lb')
        default_database.add(unit2)

        update_action = WeightUnitUpdate(default_database, [], [])

        new_name = 'kilo'
        assert new_name != self.weight_unit.name

        self.weight_unit.name = new_name

        assert default_database.query(WeightUnit).count() == 2
        _, ok = update_action(self.weight_unit)
        assert ok
        assert default_database.query(WeightUnit).count() == 2

        updated_unit = default_database.query(WeightUnit).filter(
            WeightUnit.id == self.weight_unit.id,
            WeightUnit.name == new_name
        )
        assert updated_unit.count() == 1

        stay_unit = default_database.query(WeightUnit).filter(
            WeightUnit.id == unit2.id,
            WeightUnit.name == unit2.name
        )
        assert stay_unit.count() == 1
