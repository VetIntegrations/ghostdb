from ghostdb.db.models import client
from .utils import base, generic
from .client_selectors import by_email as by_email_selector


class ClientSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, client.Client)
    by_pms_id = base.SelectorFactory(generic.ByPmsID, client.Client)
    by_email = base.SelectorFactory(by_email_selector.ByEmail, client.Client)


class ContactSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, client.ClientContact)
