from ghostdb.db.models import user
from .utils import base
from .user_selectors import getting


class UserSelector(base.BaseSelectorSet):

    by_email = base.SelectorFactory(getting.ByEmail, user.User)
