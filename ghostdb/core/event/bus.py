import abc
import json
import time
import sentry_sdk

from . import message


class BaseEventBus(abc.ABC):

    @abc.abstractmethod
    def publish(self, msg: message.BaseMessage) -> bool:
        ...


class GCPPubSubEventBus(BaseEventBus):
    REPUBLISH_MAX_TRIES = 5

    def __init__(self, gcp_project_id: str, topic: str, credentials: dict = None):
        from google.cloud import pubsub_v1

        self.client = pubsub_v1.PublisherClient(credentials=credentials)
        self.topic = self.client.topic_path(gcp_project_id, topic)

    def publish(self, msg: message.BaseMessage) -> bool:
        from google.cloud.pubsub_v1.publisher.exceptions import PublishError, TimeoutError

        result = False
        tries = self.REPUBLISH_MAX_TRIES
        while True:
            payload = json.dumps(msg.format())

            future = self.client.publish(self.topic, data=payload.encode('utf-8'))

            try:
                future.result()
                result = True
                break
            except PublishError as ex:
                sentry_sdk.capture_exception(ex)
                break
            except TimeoutError as ex:
                tries -= 1
                if tries == 0:
                    sentry_sdk.capture_exception(ex)
                    break
                else:
                    time.sleep(0.1 * (self.REPUBLISH_MAX_TRIES - tries))

        return result
