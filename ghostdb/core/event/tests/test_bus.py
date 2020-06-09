from unittest.mock import Mock
from google.cloud.pubsub_v1.publisher.exceptions import PublishError, TimeoutError

from ..bus import GCPPubSubEventBus, pubsub_v1, time


class FakeMessage:

    def __init__(self, name):
        self.name = name

    def format(self):
        return {'name': self.name}


class TestGCPPubSubEventBus:

    def test_send(self, monkeypatch):
        log = []

        class FakePublishResult:

            def result(self):
                return True

        class FakePubSub:

            def __init__(self, **kwargs):
                pass

            def topic_path(self, *args):
                return ''

            def publish(self, topic, data):
                log.append(('publish', topic, data))

                return FakePublishResult()

        monkeypatch.setattr(pubsub_v1, 'PublisherClient', FakePubSub)

        bus = GCPPubSubEventBus('test-prj', 'test-topic')
        assert bus.publish(FakeMessage('foobar'))

        assert log == [('publish', '', b'{"name": "foobar"}')]

    def test_send_error(self, monkeypatch):
        log = []

        class FakePublishResult:

            def result(self):
                raise PublishError('Test')

        class FakePubSub:

            def __init__(self, **kwargs):
                pass

            def topic_path(self, *args):
                return ''

            def publish(self, topic, data):
                log.append(('publish', topic, data))

                return FakePublishResult()

        monkeypatch.setattr(pubsub_v1, 'PublisherClient', FakePubSub)

        bus = GCPPubSubEventBus('test-prj', 'test-topic')
        assert not bus.publish(FakeMessage('foobar'))

        assert log == [('publish', '', b'{"name": "foobar"}')]

    def test_send_retries(self, monkeypatch):
        log = []

        publish_result_mock = Mock()
        publish_result_mock.result.side_effect = (
            TimeoutError('Test'),
            TimeoutError('Test'),
            True
        )

        class FakePubSub:

            def __init__(self, **kwargs):
                pass

            def topic_path(self, *args):
                return ''

            def publish(self, topic, data):
                log.append(('publish', topic, data))

                return publish_result_mock

        monkeypatch.setattr(pubsub_v1, 'PublisherClient', FakePubSub)
        monkeypatch.setattr(time, 'sleep', lambda delay: log.append(('sleep', delay)))

        bus = GCPPubSubEventBus('test-prj', 'test-topic')
        assert bus.publish(FakeMessage('foobar'))

        assert log == [
            ('publish', '', b'{"name": "foobar"}'),
            ('sleep', 0.1 * 1),
            ('publish', '', b'{"name": "foobar"}'),
            ('sleep', 0.1 * 2),
            ('publish', '', b'{"name": "foobar"}'),
        ]

    def test_send_retries_limit(self, monkeypatch):
        log = []

        publish_result_mock = Mock()
        publish_result_mock.result.side_effect = TimeoutError('Test')

        class FakePubSub:

            def __init__(self, **kwargs):
                pass

            def topic_path(self, *args):
                return ''

            def publish(self, topic, data):
                log.append(('publish', topic, data))

                return publish_result_mock

        monkeypatch.setattr(pubsub_v1, 'PublisherClient', FakePubSub)
        monkeypatch.setattr(time, 'sleep', lambda delay: log.append(('sleep', delay)))

        bus = GCPPubSubEventBus('test-prj', 'test-topic')
        assert not bus.publish(FakeMessage('foobar'))

        assert log == [
            ('publish', '', b'{"name": "foobar"}'),
            ('sleep', 0.1 * 1),
            ('publish', '', b'{"name": "foobar"}'),
            ('sleep', 0.1 * 2),
            ('publish', '', b'{"name": "foobar"}'),
            ('sleep', 0.1 * 3),
            ('publish', '', b'{"name": "foobar"}'),
            ('sleep', 0.1 * 4),
            ('publish', '', b'{"name": "foobar"}'),
        ]
