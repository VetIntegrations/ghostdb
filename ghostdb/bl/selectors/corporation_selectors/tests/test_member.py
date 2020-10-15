import uuid
import pytest

from ghostdb.db.models.corporation import Member
from ghostdb.db.models.tests.factories import UserFactory, CorporationFactory
from ..member import FindMemberByUserID


class TestFindMemberByUserID:

    def test_ok(self, dbsession):
        user = UserFactory()
        corporation = CorporationFactory()
        member = Member(corporation=corporation, user=user)
        Member(corporation=corporation, user=UserFactory())

        selector = FindMemberByUserID(dbsession, Member, None)

        assert dbsession.query(Member).count() == 2

        member_from_db, ok = selector(corporation, user.id)
        assert ok
        assert member_from_db == member

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.corporation import MemberSelector

        corporation = CorporationFactory()

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(FindMemberByUserID, 'process', process)

        with pytest.raises(Called):
            MemberSelector(dbsession).in_corporation_by_user_id(corporation, uuid.uuid1())
