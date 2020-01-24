import typing

from ghostdb.db.models import pet
from ..utils import base


class PetDelete(base.BaseAction):

    def process(self, _pet: pet.Pet) -> typing.Tuple[pet.Pet, bool]:
        self.db.delete(_pet)
        self.db.commit()

        return (_pet, True)


class BreedDelete(base.BaseAction):

    def process(self, breed: pet.Breed) -> typing.Tuple[pet.Breed, bool]:
        self.db.delete(breed)
        self.db.commit()

        return (breed, True)


class ColorDelete(base.BaseAction):

    def process(self, color: pet.Color) -> typing.Tuple[pet.Color, bool]:
        self.db.delete(color)
        self.db.commit()

        return (color, True)


class GenderDelete(base.BaseAction):

    def process(self, gender: pet.Gender) -> typing.Tuple[pet.Gender, bool]:
        self.db.delete(gender)
        self.db.commit()

        return (gender, True)


class SpeciesDelete(base.BaseAction):

    def process(self, species: pet.Species) -> typing.Tuple[pet.Species, bool]:
        self.db.delete(species)
        self.db.commit()

        return (species, True)


class WeightUnitDelete(base.BaseAction):

    def process(self, unit: pet.WeightUnit) -> typing.Tuple[pet.WeightUnit, bool]:
        self.db.delete(unit)
        self.db.commit()

        return (unit, True)
