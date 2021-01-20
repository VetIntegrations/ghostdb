from ghostdb.db.models import user
from .utils import base, generic
from .user_selectors import getting, by_deleted, by_not_verification_email


class UserSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, user.User)
    by_email = base.SelectorFactory(getting.ByEmail, user.User)
    by_deleted = base.SelectorFactory(by_deleted.FindDeletedUsers, user.User)
    by_not_verification_email = base.SelectorFactory(by_not_verification_email.FindNotVerificationUsers, user.User)
