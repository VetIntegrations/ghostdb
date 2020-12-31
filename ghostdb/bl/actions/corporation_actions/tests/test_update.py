import pytest
from uuid import UUID
from sqlalchemy_utils.primitives import Ltree

from ghostdb.db.models.corporation import Corporation, Member
from ghostdb.db.models.user import User
from ghostdb.db.models.tests.factories import (
    CorporationFactory, UserFactory, TemporaryTokenFactory, MemberFactory
)
from ghostdb.bl.actions.corporation import CorporationAction, OrgChartAction
from ..update import (
    Update, UpdateMember, ActivateMember, OrgChartRemoveUser, OrgChartMoveMember
)


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
            user=UserFactory(),
            role='CEO'
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
            user=UserFactory(),
            role='IT'
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

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(ActivateMember, 'process', process)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.activate_member(MemberFactory())

    def test_activate(self, dbsession, event_off):
        user = UserFactory()
        member = MemberFactory(user=None, role='CEO')

        assert not member.is_active
        assert not member.date_of_join
        assert not user.date_of_join

        assert dbsession.query(Member).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        member_db, ok = action.activate_member(member, user=user)
        assert ok
        assert dbsession.query(Member).count() == 1
        event_off.assert_called_once()

        assert member_db.id == member.id
        assert member_db.is_active
        assert member_db.date_of_join
        assert member_db.user == user
        assert not user.date_of_join

    def test_activate_by_invite(self, dbsession, event_off):
        corp = CorporationFactory()
        user = UserFactory(corporation=None)

        invite = TemporaryTokenFactory(user=user, extra={'corporation': corp.id.hex})
        member = MemberFactory(user=user, corporation=None, role='CEO', invite=invite)

        assert not member.is_active
        assert not member.date_of_join
        assert not user.date_of_join
        assert member.invite

        assert dbsession.query(Member).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        member_db, ok = action.activate_member(member, invite=invite)
        assert ok
        assert member_db == member
        assert dbsession.query(Member).count() == 1
        event_off.assert_called_once()

        updated_member = dbsession.query(Member)[0]
        updated_user = dbsession.query(User)[0]

        assert updated_member.id == member.id
        assert updated_member.is_active
        assert updated_member.invite is None
        assert updated_member.date_of_join
        assert updated_member.corporation == corp

        assert updated_user.id == user.id
        assert updated_user.date_of_join
        assert updated_user.corporation == corp


class TestOrgChartRemoveUser:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = CorporationFactory()
        self.user = UserFactory()
        self.member = MemberFactory(
            corporation=self.corp,
            user=self.user,
            role='CEO'
        )

    def test_remove_from_corp(self, dbsession, event_off):
        assert dbsession.query(Member).count() == 1
        assert dbsession.query(Member).filter(Member.user == self.user).count() == 1

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        cnt, ok = action.remove_user(self.user)

        assert dbsession.query(Member).count() == 1
        assert dbsession.query(Member).filter(Member.user == self.user).count() == 0

    def test_remove_from_exact_corporation(self, dbsession, event_off):
        new_corp = CorporationFactory()
        MemberFactory(corporation=new_corp, user=self.user, role='IT')

        assert dbsession.query(Member).count() == 2
        assert dbsession.query(Member).filter(Member.user == self.user).count() == 2

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        cnt, ok = action.remove_user(self.user, self.corp)

        assert dbsession.query(Member).count() == 2
        assert dbsession.query(Member).filter(Member.user == self.user).count() == 1
        assert dbsession.query(Member).filter(Member.user == self.user, Member.corporation == new_corp).count() == 1

    def test_remove_from_except_exact_member(self, dbsession, event_off):
        MemberFactory(corporation=CorporationFactory(), user=self.user, role='HR')
        new_corp = CorporationFactory()
        member = MemberFactory(corporation=new_corp, user=self.user, role='IT')

        assert dbsession.query(Member).count() == 3
        assert dbsession.query(Member).filter(Member.user == self.user).count() == 3

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        cnt, ok = action.remove_user(self.user, except_members=[member.id.hex])

        assert dbsession.query(Member).count() == 3
        assert dbsession.query(Member).filter(Member.user == self.user).count() == 1
        assert dbsession.query(Member).filter(Member.user == self.user, Member.corporation == new_corp).count() == 1

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrgChartRemoveUser, 'process', process)

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.remove_user(self.user)


class TestOrgChartMoveMember:

    @pytest.fixture(autouse=True)
    def setup_orgchart(self, dbsession):
        self.corporation = CorporationFactory()
        self.ceo = MemberFactory(role='ceo', corporation=self.corporation)
        self.hr_manager = MemberFactory(
            id=UUID('45cfc2c2-45d3-11eb-8157-f40f2436dd91'),
            role='hr manager', path=Ltree(self.ceo.id.hex), corporation=self.corporation
        )
        self.accounting = MemberFactory(
            id=UUID('4651374e-45d3-11eb-8157-f40f2436dd91'),
            role='accounting', path=Ltree(self.ceo.id.hex), corporation=self.corporation
        )

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(OrgChartMoveMember, 'process', process)

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.move_member(self.accounting, parent=self.hr_manager)

    def test_move_single_member_to_new_parent(self, dbsession, event_off):
        member = MemberFactory(
            role='worker',
            path=Ltree(self.ceo.id.hex + '.' + self.hr_manager.id.hex),
            corporation=self.corporation
        )

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = member.path
        member, ok = action.move_member(member, new_parent=self.accounting)

        assert member.path != old_path
        assert member.path == Ltree(self.ceo.id.hex) + Ltree(self.accounting.id.hex)

    def test_move_member_with_subordinates_to_new_parent(self, dbsession, event_off):
        member = MemberFactory(
            role='manager',
            path=Ltree(self.ceo.id.hex),
            corporation=self.corporation
        )
        subordinate1 = MemberFactory(
            role='worker 1',
            path=member.path + Ltree(member.id.hex),
            corporation=self.corporation
        )
        subordinate12 = MemberFactory(
            role='worker 1.2',
            path=subordinate1.path + Ltree(subordinate1.id.hex),
            corporation=self.corporation
        )

        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = member.path
        member, ok = action.move_member(member, new_parent=self.accounting)

        new_parent_path = Ltree(self.ceo.id.hex) + Ltree(self.accounting.id.hex)
        assert member.path != old_path
        assert member.path == new_parent_path

        assert subordinate1.path == new_parent_path + Ltree(member.id.hex)
        assert subordinate12.path == new_parent_path + Ltree(member.id.hex) + Ltree(subordinate1.id.hex)
