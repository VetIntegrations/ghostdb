from ghostdb.db.models import provider
from .utils import base, generic


class ProviderSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, provider.Provider)


class ProviderKindSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, provider.ProviderKind)
    by_iname = base.SelectorFactory(generic.ByIName, provider.ProviderKind)
