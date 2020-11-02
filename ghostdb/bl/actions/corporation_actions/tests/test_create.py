import pytest

from ghostdb.db.models.corporation import Corporation, Member
from ghostdb.db.models.tests.factories import UserFactory
from ghostdb.bl.actions.corporation import CorporationAction
from ..create import Create, AddMember


class TestCorporationCreate:

    def test_ok(self, dbsession, event_off):
        corp = Corporation(name='Test Corp 1')

        assert dbsession.query(Corporation).count() == 0
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        new_corp, ok = action.create(corp)
        assert ok
        assert new_corp == corp
        assert dbsession.query(Corporation).count() == 1
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Create, 'process', process)

        corp = Corporation(name='Test Corp 1')
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.create(corp)


class TestCorporationAddMember:

    @pytest.fixture(autouse=True)
    def setup_corp(self, dbsession):
        self.corp = Corporation(name='Test Corp 1')
        dbsession.add(self.corp)
        dbsession.commit()

    @pytest.fixture(autouse=True)
    def setup_user(self, dbsession):
        self.user = UserFactory()
        dbsession.add(self.user)
        dbsession.commit()

    def test_ok(self, dbsession, event_off):
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')

        assert dbsession.query(Member).count() == 0
        member = Member(user=self.user)
        new_member, ok = action.add_member(self.corp, member)
        assert ok
        assert new_member == member
        assert new_member.corporation == self.corp
        assert dbsession.query(Member).count() == 1

        event_off.assert_called_once()

    def test_build_path(self, dbsession, event_off):
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')

        assert dbsession.query(Member).count() == 0

        member_lvl_0 = Member()
        member_lvl_1 = Member()
        member_lvl_2 = Member()

        action.add_member(self.corp, member_lvl_0)
        action.add_member(self.corp, member_lvl_1, member_lvl_0)
        action.add_member(self.corp, member_lvl_2, member_lvl_1)

        assert dbsession.query(Member).count() == 3
        assert member_lvl_0.path is None
        assert member_lvl_1.path == member_lvl_0.id.hex
        assert member_lvl_2.path == f'{member_lvl_0.id.hex}.{member_lvl_1.id.hex}'

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(AddMember, 'process', process)

        member = Member(user=self.user)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.add_member(self.corp, member)
