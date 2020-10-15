import uuid
import pytest

from ghostdb.db.models.corporation import Member
from ghostdb.db.models.tests.factories import MemberFactory, CorporationFactory, UserFactory
from ..member import FindMemberByUserID, ActiveByUserID


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


class TestActiveByUserID:

    def test_ok(self, dbsession):
        user = UserFactory()
        member = MemberFactory(user=user, is_active=True)

        selector = ActiveByUserID(dbsession, Member, None)

        assert dbsession.query(Member).count() == 1

        member_from_db, ok = selector(user.id)
        assert ok
        assert member_from_db == member

    def test_only_active(self, dbsession):
        user = UserFactory()
        MemberFactory(user=user, is_active=False)

        selector = ActiveByUserID(dbsession, Member, None)

        assert dbsession.query(Member).count() == 1

        member_from_db, ok = selector(user.id)
        assert not ok
        assert member_from_db is None

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.corporation import MemberSelector

        corporation = CorporationFactory()

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ActiveByUserID, 'process', process)

        with pytest.raises(Called):
            MemberSelector(dbsession).active_by_user_id(corporation, uuid.uuid1())
