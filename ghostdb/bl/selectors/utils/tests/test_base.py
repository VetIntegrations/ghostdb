from ..base import BaseSelectorSet, BaseSelector, SelectorFactory


def test_selector_factory():
    class Selector(BaseSelector):
        called = False

        def process(self, *args, **kwargs):
            self.__class__.called = True
            return (None, True)

    class Model:
        ...

    class SelectorSet(BaseSelectorSet):
        test_selector = SelectorFactory(Selector, Model)

    selectorset = SelectorSet(None)
    assert not selectorset.test_selector.called
    selectorset.test_selector()
    assert selectorset.test_selector.called


def test_base_selector_workflow():
    log = []

    class Selector(BaseSelector):

        def process(self, *args, **kwargs):
            log.append(('Selector.process', args, kwargs))
            return (None, True)

    selector = Selector(None, None, None)

    assert len(log) == 0
    selector()
    assert log == [
        ('Selector.process', tuple(), {}),
    ]
