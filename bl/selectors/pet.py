from ghostdb.db.models import pet
from .utils import base, generic


class PetSelector:

    by_id = base.selector_factory(generic.ByID, pet.Pet)
