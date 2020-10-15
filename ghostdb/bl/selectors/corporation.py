from ghostdb.db.models import corporation
from .utils import base, generic
from .corporation_selectors import member


class CorporationSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, corporation.Corporation)
    by_iname = base.SelectorFactory(generic.ByIName, corporation.Corporation)


class MemberSelector(base.BaseSelectorSet):

    by_id = base.SelectorFactory(generic.ByID, corporation.Member)
    by_invite_id = base.SelectorFactory(member.ByInviteID, corporation.Member)
    in_corporation_by_user_id = base.SelectorFactory(member.FindMemberByUserID, corporation.Member)
