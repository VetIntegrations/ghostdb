import uuid
import pytest

from ghostdb.db.models import pet as pet_models
from .. import pet as pet_selectors


class TestByID:

    @pytest.fixture(autouse=True)
    def setup_pet(self, dbsession):
        self.pet = pet_models.Pet(name='Ricky')
        dbsession.add(self.pet)
        dbsession.commit()

    def test_ok(self, dbsession):
        pet, ok = pet_selectors.PetSelector(dbsession).by_id(self.pet.id)

        assert ok
        assert pet.id == self.pet.id
        assert pet.name == self.pet.name

    def test_not_found(self, dbsession):
        pet, ok = pet_selectors.PetSelector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert pet is None


@pytest.mark.parametrize(
    'model, selector',
    (
        (pet_models.Breed, pet_selectors.BreedSelector),
        (pet_models.Color, pet_selectors.ColorSelector),
        (pet_models.Gender, pet_selectors.GenderSelector),
        (pet_models.Species, pet_selectors.SpeciesSelector),
        (pet_models.WeightUnit, pet_selectors.WeightUnitSelector),
    )
)
class PetRelatedObjectsTest:

    @pytest.fixture(autouse=True)
    def setup(self, model, selector, dbsession):
        self.obj = model(name='FooBar')
        dbsession.add(self.obj)
        dbsession.commit()

    def test_get_by_id(self, model, selector, dbsession):
        obj, ok = selector(dbsession).by_id(self.obj.id)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_get_by_id_not_found(self, model, selector, dbsession):
        obj, ok = selector(dbsession).by_id(uuid.uuid4())

        assert not ok
        assert obj is None

    def test_get_by_name(self, model, selector, dbsession):
        obj, ok = selector(dbsession).by_id(self.obj.name)

        assert ok
        assert obj.id == self.obj.id
        assert obj.name == self.obj.name

    def test_get_by_name_not_found(self, model, selector, dbsession):
        obj, ok = selector(dbsession).by_id('FooBuz')

        assert not ok
        assert obj is None
