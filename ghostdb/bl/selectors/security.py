from ghostdb.db.models import security
from .utils import base
from .security_selectors import by_token, by_time, by_user


class TemporaryTokenSelector(base.BaseSelectorSet):

    by_token_utc = base.SelectorFactory(by_token.TemporaryTokenByTokenUtc, security.TemporaryToken)

    all_expired = base.SelectorFactory(by_time.TemporaryTokenExpired, security.TemporaryToken)
    filter_by_expire_date = base.SelectorFactory(
        by_time.TemporaryTokenFilterByExpireDate,
        security.TemporaryToken
    )
    active_by_user = base.SelectorFactory(by_user.TemporatyTokenActiveByUser, security.TemporaryToken)
