from ghostdb.db.models import corporation
from .utils import base, generic


class CorporationSelector:

    by_id = base.selector_factory(generic.ByID, corporation.Corporation)
