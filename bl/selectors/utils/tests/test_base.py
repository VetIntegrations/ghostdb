import pytest

from ghostdb.exceptions import NoDefaultDatabase
from ..base import BaseSelector, selector_factory


class TestSelectorFactory:

    def test_selector_factory(self, mock_default_database):
        class Selector(BaseSelector):
            called = False

            def process(self, *args, **kwargs):
                self.called = True
                return (None, True)

        class Model:
            ...

        selector = selector_factory(Selector, Model)
        assert not selector.called
        selector(None)
        assert selector.called

    def test_no_default_db(self):
        class Selector(BaseSelector):
            ...

        class Model:
            ...

        with pytest.raises(NoDefaultDatabase):
            selector_factory(Selector, Model)


def test_base_selector_workflow():
    log = []

    class Selector(BaseSelector):

        def process(self, *args, **kwargs):
            log.append(('Selector.process', args, kwargs))
            return (None, True)

    selector = Selector(None, None)

    assert len(log) == 0
    selector()
    assert log == [
        ('Selector.process', tuple(), {}),
    ]
