from ghostdb.db.models import business
from .utils import base, generic


class BusinessSelector:

    by_id = base.selector_factory(generic.ByID, business.Business)
