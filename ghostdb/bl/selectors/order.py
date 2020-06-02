from ghostdb.db.models import order
from .utils import base, generic


class OrderSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, order.Order)
