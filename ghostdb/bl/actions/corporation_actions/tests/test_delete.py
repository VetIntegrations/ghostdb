import pytest

from sqlalchemy_utils.primitives import Ltree

from ghostdb.db.models.corporation import Corporation, Member
from ghostdb.bl.actions.corporation import CorporationAction
from ghostdb.db.models.tests.factories import MemberFactory, CorporationFactory, UserFactory
from ..delete import Delete, DeleteMember


class TestCorporationDelete:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = Corporation(name='Test Corporation')
        dbsession.add(self.corp)

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Corporation).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.corp)
        assert ok
        assert dbsession.query(Corporation).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(Delete, 'process', process)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete(self.corp)

    def test_delete_right_record(self, dbsession, event_off):
        corp = Corporation(name='Test Corporation Stay')
        dbsession.add(corp)

        assert dbsession.query(Corporation).count() == 2
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete(self.corp)
        assert ok
        assert dbsession.query(Corporation).count() == 1

        assert dbsession.query(Corporation)[0] == corp


class TestMemberDelete:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.member = MemberFactory(
            corporation=CorporationFactory(),
            user=UserFactory()
        )

    def test_ok(self, dbsession, event_off):
        assert dbsession.query(Member).count() == 1
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete_member(self.member)
        assert ok
        assert dbsession.query(Member).count() == 0
        event_off.assert_called_once()

    def test_action_class_use_right_action(self, dbsession, monkeypatch):
        class Called(Exception):
            ...

        def process(self, *args, **kwargs):
            raise Called()

        monkeypatch.setattr(DeleteMember, 'process', process)

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        with pytest.raises(Called):
            action.delete_member(self.member)

    def test_delete_right_record(self, dbsession, event_off):
        member = MemberFactory(
            corporation=CorporationFactory(),
            user=UserFactory()
        )

        assert dbsession.query(Member).count() == 2
        action = CorporationAction(dbsession, event_bus=None, customer_name='test-cosolidator')
        _, ok = action.delete_member(self.member)
        assert ok
        assert dbsession.query(Member).count() == 1

        assert dbsession.query(Member)[0] == member

    def test_rebuild_path_for_subordinates(self, dbsession, event_off):
        corporation = CorporationFactory()

        ceo = MemberFactory(
            role='ceo',
            corporation=corporation
        )

        manager = MemberFactory(
            role='manager',
            path=Ltree(ceo.id.hex),
            corporation=corporation
        )
        subordinate1 = MemberFactory(
            role='worker 1',
            path=manager.path + Ltree(manager.id.hex),
            corporation=corporation
        )
        subordinate12 = MemberFactory(
            role='worker 1.2',
            path=subordinate1.path + Ltree(subordinate1.id.hex),
            corporation=corporation
        )

        dbsession.commit()

        action = CorporationAction(dbsession, event_bus=None, customer_name='test-consolidator')
        action.delete_member(manager)

        # check that manager was deleted
        assert not dbsession.query(Member).get(manager.id)

        # check that subordinate1 and subordinate12 existed in the db
        assert dbsession.query(Member).get(subordinate1.id) == subordinate1
        assert dbsession.query(Member).get(subordinate12.id) == subordinate12

        # check that subordinate1 and subordinate12 have new parent
        assert subordinate1.path == Ltree(ceo.id.hex)
        assert subordinate12.path == Ltree(ceo.id.hex) + Ltree(subordinate1.id.hex)
