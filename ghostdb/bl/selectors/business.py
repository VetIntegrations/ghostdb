from ghostdb.db.models import business
from .utils import base, generic


class BusinessSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, business.Business)
