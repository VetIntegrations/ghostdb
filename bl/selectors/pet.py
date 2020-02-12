from ghostdb.db.models import pet
from .utils import base, generic


class PetSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, pet.Pet)


class BreedSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, pet.Breed)
    by_iname = base.SelectorFactory(generic.ByIName, pet.Breed)


class ColorSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, pet.Color)
    by_iname = base.SelectorFactory(generic.ByIName, pet.Color)


class GenderSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, pet.Gender)
    by_iname = base.SelectorFactory(generic.ByIName, pet.Gender)


class SpeciesSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, pet.Species)
    by_iname = base.SelectorFactory(generic.ByIName, pet.Species)


class WeightUnitSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, pet.WeightUnit)
    by_iname = base.SelectorFactory(generic.ByIName, pet.WeightUnit)
