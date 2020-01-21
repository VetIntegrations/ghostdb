from ghostdb.db.models import client
from .utils import base, generic
from .client_selectors import by_email as by_email_selector


class ClientSelector:

    by_id = base.selector_factory(generic.ByID, client.Client)
    by_email = base.selector_factory(by_email_selector.ByEmail, client.Client)
