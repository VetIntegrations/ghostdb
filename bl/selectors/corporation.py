from ghostdb.db.models import corporation
from .utils import base, generic


class CorporationSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, corporation.Corporation)
