from ghostdb.db.models import user
from .utils import base, generic
from .user_selectors import getting, by_deleted


class UserSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, user.User)
    by_email = base.SelectorFactory(getting.ByEmail, user.User)
    by_deleted = base.SelectorFactory(by_deleted.FindDeletedUsers, user.User)
