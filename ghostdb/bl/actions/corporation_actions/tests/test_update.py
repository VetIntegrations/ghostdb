import pytest

from ghostdb.db.models.corporation import Corporation, Member
from ghostdb.db.models.tests.factories import CorporationFactory, UserFactory, TemporaryTokenFactory
from ghostdb.bl.actions.corporation import CorporationAction
from ..update import Update, UpdateMember, ActivateMember


class TestCorporationUpdate:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation')
        dbsession.add(self.corp)

    def test_ok(self, dbsession, event_off):
        new_name = 'John Doe Inc.'
        assert new_name != self.corp.name

        self.corp.name = new_name

        assert dbsession.query(Corporation).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        corp, ok = action.update(self.corp)
        assert ok
        assert corp == self.corp
        assert dbsession.query(Corporation).count() == 1
        event_off.assert_called_once()

        updated_corp = dbsession.query(Corporation)[0]
        assert updated_corp.id == self.corp.id
        assert updated_corp.name == new_name

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Update, 'process', process)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update(self.corp)

    def test_update_right_record(self, dbsession, event_off):
        corp = Corporation(name='Stay Corp.')
        dbsession.add(corp)

        new_name = 'John Doe Inc.'
        assert new_name != self.corp.name

        self.corp.name = new_name

        assert dbsession.query(Corporation).count() == 2
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update(self.corp)
        assert ok
        assert dbsession.query(Corporation).count() == 2

        updated_corp = dbsession.query(Corporation).filter(
            Corporation.id == self.corp.id,
            Corporation.name == new_name
        )
        assert updated_corp.count() == 1

        stay_corp = dbsession.query(Corporation).filter(
            Corporation.id == corp.id,
            Corporation.name == corp.name
        )
        assert stay_corp.count() == 1


class TestUpdateMember:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation')
        self.member = Member(
            corporation=self.corp,
            user=UserFactory()
        )
        dbsession.add(self.corp)
        dbsession.add(self.member)

    def test_ok(self, dbsession, event_off):
        assert not self.member.is_active

        self.member.is_active = True

        assert dbsession.query(Member).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        member, ok = action.update_member(self.member)
        assert ok
        assert member == self.member
        assert dbsession.query(Member).count() == 1
        event_off.assert_called_once()

        updated_member = dbsession.query(Member)[0]
        assert updated_member.id == self.member.id
        assert updated_member.is_active

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(UpdateMember, 'process', process)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.update_member(self.member)

    def test_update_right_record(self, dbsession, event_off):
        other_member = Member(
            corporation=self.corp,
            user=UserFactory()
        )
        dbsession.add(other_member)

        assert not self.member.is_active
        assert not other_member.is_active

        self.member.is_active = True

        assert dbsession.query(Member).count() == 2
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.update_member(self.member)
        assert ok
        assert dbsession.query(Member).count() == 2

        updated_member = dbsession.query(Member).filter(
            Member.id == self.member.id,
            Member.is_active.is_(True)
        )
        assert updated_member.count() == 1

        stay_member = dbsession.query(Member).filter(
            Member.id == other_member.id,
            Member.is_active.is_(False)
        )
        assert stay_member.count() == 1


class TestActivateMember:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = CorporationFactory()
        user = UserFactory()
        self.member = Member(
            corporation=self.corp,
            user=user,
            invite=TemporaryTokenFactory(user=user, extra={'corporation': self.corp.id.hex})
        )
        dbsession.add(self.corp)
        dbsession.add(self.member)

    def test_ok(self, dbsession, event_off):
        assert not self.member.is_active
        assert not self.member.date_of_join
        assert self.member.invite

        assert dbsession.query(Member).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        member, ok = action.activate_member(self.member)
        assert ok
        assert member == self.member
        assert dbsession.query(Member).count() == 1
        event_off.assert_called_once()

        updated_member = dbsession.query(Member)[0]
        assert updated_member.id == self.member.id
        assert updated_member.is_active
        assert updated_member.invite is None
        assert updated_member.date_of_join

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ActivateMember, 'process', process)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.activate_member(self.member)

    def test_join_corporation_from_invite(self, dbsession, event_off):
        other_corp = CorporationFactory()

        assert not self.member.is_active
        assert not self.member.date_of_join
        assert self.member.invite

        self.member.invite.extra['corporation'] = other_corp.id.hex

        assert dbsession.query(Member).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        member, ok = action.activate_member(self.member)
        assert ok
        assert member == self.member
        assert dbsession.query(Member).count() == 1
        event_off.assert_called_once()

        updated_member = dbsession.query(Member)[0]
        assert updated_member.id == self.member.id
        assert updated_member.is_active
        assert updated_member.invite is None
        assert updated_member.date_of_join
        assert updated_member.corporation == other_corp
