import typing

from ghostdb.db.models import pet
from ..utils import base


class Delete(base.BaseAction):

    def process(self, _pet: pet.Pet) -> typing.Tuple[pet.Pet, bool]:
        self.db.delete(_pet)
        self.db.commit()

        return (_pet, True)
