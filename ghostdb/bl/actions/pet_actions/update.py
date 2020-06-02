import typing

from ghostdb.db.models import pet
from ..utils import base


class PetUpdate(base.BaseAction):

    def process(self, _pet: pet.Pet) -> typing.Tuple[pet.Pet, bool]:
        self.db.add(_pet)
        self.db.commit()

        return (_pet, True)


class BreedUpdate(base.BaseAction):

    def process(self, breed: pet.Breed) -> typing.Tuple[pet.Breed, bool]:
        self.db.add(breed)
        self.db.commit()

        return (breed, True)


class ColorUpdate(base.BaseAction):

    def process(self, color: pet.Color) -> typing.Tuple[pet.Color, bool]:
        self.db.add(color)
        self.db.commit()

        return (color, True)


class GenderUpdate(base.BaseAction):

    def process(self, gender: pet.Gender) -> typing.Tuple[pet.Gender, bool]:
        self.db.add(gender)
        self.db.commit()

        return (gender, True)


class SpeciesUpdate(base.BaseAction):

    def process(self, species: pet.Species) -> typing.Tuple[pet.Species, bool]:
        self.db.add(species)
        self.db.commit()

        return (species, True)


class WeightUnitUpdate(base.BaseAction):

    def process(self, unit: pet.WeightUnit) -> typing.Tuple[pet.WeightUnit, bool]:
        self.db.add(unit)
        self.db.commit()

        return (unit, True)
