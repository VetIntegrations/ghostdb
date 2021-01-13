import pytest
from sqlalchemy_utils.primitives import Ltree

from ghostdb.db.models.tests.factories import CorporationFactory, MemberFactory
from ghostdb.bl.actions.corporation import OrgChartAction


class TestReorderMembers:

    @pytest.fixture(autouse=True)
    def setup_corporation(self, dbsession):
        self.corp = CorporationFactory(name='Test Corporation')
        self.ceo = MemberFactory(
            corporation=self.corp,
            role='CEO'
        )
        dbsession.add(self.corp)
        dbsession.add(self.ceo)

    def _create_orgchart(self, left_ordering: int = 100, right_ordering: int = 200):
        self.hr = MemberFactory(
            corporation=self.corp,
            role='HR',
            path=Ltree(self.ceo.id.hex),
            ordering=left_ordering
        )
        self.legal = MemberFactory(
            corporation=self.corp,
            role='Legal',
            path=Ltree(self.ceo.id.hex),
            ordering=right_ordering
        )
        self.member = MemberFactory(
            corporation=self.corp,
            role='Member',
            path=Ltree(self.ceo.id.hex),
            ordering=500
        )

    def test_insert_to_parent(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo
        )

        assert member.ordering == 0
        assert member.path == old_path
        assert self.hr.ordering == 200
        assert self.legal.ordering == 300

    def test_insert_to_parent_wihtout_children(self, dbsession, event_off):
        member = MemberFactory(
            corporation=self.corp,
            role='Member',
            path=Ltree(self.ceo.id.hex),
            ordering=500
        )
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = member.path
        member, ok = action.move_member(
            member,
            new_parent=self.ceo
        )

        assert member.ordering == 0
        assert member.path == old_path

    def test_insert_between_left_and_right_neighbors(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            left_neighbor=self.hr,
            right_neighbor=self.legal
        )

        assert member.ordering == 150
        assert member.path == old_path

    def test_insert_between_left_and_right_neighbors_wrong_ordering(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            left_neighbor=self.legal,
            right_neighbor=self.hr
        )

        assert member.ordering == 150
        assert member.path == old_path

    @pytest.mark.parametrize(
        'left_ordering, right_ordering, expected_ordering',
        (
            (100, 100, 150),
            (50, 51, 100),
        )
    )
    def test_insert_between_left_and_right_neighbors_without_empty_space(
        self,
        left_ordering, right_ordering, expected_ordering,
        dbsession, event_off
    ):
        self._create_orgchart(left_ordering=left_ordering, right_ordering=right_ordering)
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            left_neighbor=self.hr,
            right_neighbor=self.legal
        )

        assert member.ordering == expected_ordering
        assert member.path == old_path
        assert self.hr.ordering == left_ordering
        assert self.legal.ordering == right_ordering + 100

    def test_insert_with_left_neighbor_when_right_exists(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            left_neighbor=self.hr
        )

        assert member.ordering == 150
        assert member.path == old_path
        assert self.hr.ordering == 100
        assert self.legal.ordering == 200

    def test_insert_with_left_neighbor_when_right_does_not_exists(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            left_neighbor=self.legal
        )

        assert member.ordering == 300
        assert member.path == old_path
        assert self.hr.ordering == 100
        assert self.legal.ordering == 200

    def test_insert_with_right_neighbor_when_left_exists(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            right_neighbor=self.legal
        )

        assert member.ordering == 150
        assert member.path == old_path
        assert self.hr.ordering == 100
        assert self.legal.ordering == 200

    def test_insert_with_right_neighbor_when_left_does_not_exists(self, dbsession, event_off):
        self._create_orgchart()
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            right_neighbor=self.hr
        )

        assert member.ordering == 0
        assert member.path == old_path
        assert self.hr.ordering == 200
        assert self.legal.ordering == 300

    def test_insert_with_right_neighbor_when_on_left_few_neighbors(self, dbsession, event_off):
        self._create_orgchart(left_ordering=100, right_ordering=200)
        MemberFactory(
            corporation=self.corp,
            role='Operations',
            path=Ltree(self.ceo.id.hex),
            ordering=50
        )
        dbsession.commit()

        action = OrgChartAction(dbsession, event_bus=None, customer_name='test-consolidator')
        old_path = self.member.path
        member, ok = action.move_member(
            self.member,
            new_parent=self.ceo,
            right_neighbor=self.legal
        )

        assert member.ordering == 150
        assert member.path == old_path
        assert self.hr.ordering == 100
        assert self.legal.ordering == 200
