import pytest

from ghostdb.db.models.code import RevenueCenter
from ..by_name import ByName


class TestSelectByName:

    @pytest.fixture(autouse=True)
    def setup_revenuecenter(self, default_database):
        self.revenue_center = RevenueCenter(name='FooBar')
        default_database.add(self.revenue_center)

    def test_ok(self, default_database):
        selector = ByName(default_database, RevenueCenter)

        assert default_database.query(RevenueCenter).count() == 1
        revenue_center, ok = selector(self.revenue_center.name)
        assert ok
        assert revenue_center == self.revenue_center

    def test_get_right_record(self, default_database):
        revenue_center2 = RevenueCenter(name='FooBaz')
        default_database.add(revenue_center2)

        selector = ByName(default_database, RevenueCenter)

        assert default_database.query(RevenueCenter).count() == 2
        revenue_center, ok = selector(self.revenue_center.name)
        assert ok
        assert revenue_center == self.revenue_center


@pytest.mark.parametrize(
    'selector_class_name',
    (
        'RevenueCenterSelector',
        'DepartmentSelector',
        'CategorySelector',
        'ClassSelector',
        'SubClassSelector',
        'ServiceTypeSelector',
        'ServiceSelector',
    )
)
def test_selector_class_use_right_selector(
    selector_class_name,
    default_database,
    monkeypatch
):
    from ghostdb.bl.selectors import code

    class Called(Exception):
        ...

    def process(self, *args, **kwargs):
        raise Called()

    monkeypatch.setattr(ByName, 'process', process)

    with pytest.raises(Called):
        getattr(code, selector_class_name).by_name()
