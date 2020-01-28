from ghostdb.db.models import provider
from .utils import base, generic


class ProviderSelector:

    by_id = base.selector_factory(generic.ByID, provider.Provider)
