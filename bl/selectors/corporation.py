from ghostdb.db.models import corporation
from .utils import base
from .corporation_selectors import (
    by_id as by_id_selector
)


class CorporationSelector:

    by_id = base.selector_factory(by_id_selector.ByID, corporation.Corporation)
