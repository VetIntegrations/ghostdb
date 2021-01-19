import uuid
import pytest

from ghostdb.db.models.corporation import Member
from ghostdb.db.models.tests.factories import (
    MemberFactory, CorporationFactory, UserFactory, TemporaryTokenFactory
)
from ..member import FindMembersByUserID, ActiveByUserID, WithInviteForEmails


class TestFindMembersByUserID:

    def test_ok(self, dbsession):
        user = UserFactory()
        corporation = CorporationFactory()
        member_1 = Member(corporation=corporation, user=user, role='CEO')
        member_2 = Member(corporation=corporation, user=user, role='IT')
        Member(corporation=corporation, user=UserFactory(), role='HR')

        selector = FindMembersByUserID(dbsession, Member, None)

        assert dbsession.query(Member).count() == 3

        members_from_db = selector(corporation, user.id)
        assert members_from_db.all() == [member_1, member_2, ]

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.corporation import MemberSelector

        corporation = CorporationFactory()

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(FindMembersByUserID, 'process', process)

        with pytest.raises(Called):
            MemberSelector(dbsession).in_corporation_by_user_id(corporation, uuid.uuid1())


class TestActiveByUserID:

    def test_ok(self, dbsession):
        user = UserFactory()
        member = MemberFactory(user=user, is_active=True, role='CEO')

        selector = ActiveByUserID(dbsession, Member, None)

        assert dbsession.query(Member).count() == 1

        member_from_db, ok = selector(user.id)
        assert ok
        assert member_from_db == member

    def test_only_active(self, dbsession):
        user = UserFactory()
        MemberFactory(user=user, is_active=False, role='CEO')

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


class TestWithInviteForEmails:

    def test_ok(self, dbsession):
        user = UserFactory()
        token = TemporaryTokenFactory(
            user=user,
            corporation=user.corporation,
            extra={'email': user.email},
        )
        member = MemberFactory(role='t', user=user, corporation=user.corporation, invite=token)
        selector = WithInviteForEmails(dbsession, Member, None)

        assert dbsession.query(Member).count() == 1

        member_from_db, ok = selector(token.user.corporation, [token.user.email])
        assert ok
        assert member_from_db.all() == [member]

    def test_filtering(self, dbsession):
        user = UserFactory()
        token = TemporaryTokenFactory(
            user=user,
            corporation=user.corporation,
            extra={'email': user.email},
        )
        member1 = MemberFactory(role='t', user=user, corporation=user.corporation, invite=token)
        member2 = MemberFactory(role='tt', user=user, corporation=user.corporation, invite=token)

        # should not be in the list
        MemberFactory(role='z', user=user, corporation=CorporationFactory(), invite=token)  # different corporeation
        token2 = TemporaryTokenFactory(
            user=user,
            corporation=user.corporation,
            extra={'email': 'foo@test'},
        )
        MemberFactory(role='t', user=user, corporation=user.corporation, invite=token2)  # different email in invite

        selector = WithInviteForEmails(dbsession, Member, None)

        assert dbsession.query(Member).count() == 4

        member_from_db, ok = selector(token.user.corporation, [token.user.email])
        assert ok
        assert member_from_db.all() == [member1, member2]

    def test_selector_class_use_right_selector(self, dbsession, monkeypatch):
        from ghostdb.bl.selectors.corporation import MemberSelector

        corporation = CorporationFactory()

        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(WithInviteForEmails, 'process', process)

        with pytest.raises(Called):
            MemberSelector(dbsession).with_invite_for_emails(corporation, ['a@localhost'])
