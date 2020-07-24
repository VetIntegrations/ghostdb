import uuid
from collections import namedtuple
from unittest.mock import Mock

from ..message import InternalMessage


DataObj = namedtuple('DataObj', 'id')


class TestMessage:

    def test_without_data(self):

        obj = DataObj(uuid.uuid4())
        msg = InternalMessage(
            customer='test-customer',
            event_name='event.create',
            obj=obj,
            data=None
        )

        assert msg.format() == {
            'customer': 'test-customer',
            'meta': {
                'event_name': 'event.create',
                'obj': {
                    'model': 'ghostdb.core.event.tests.test_message.DataObj',
                    'pk': obj.id.hex,
                },
            },
        }

    def test_with_data(self):

        obj = DataObj(uuid.uuid4())
        data = {'name': 'Foo', 'alias': 'Bar'}
        msg = InternalMessage(
            customer='test-customer',
            event_name='event.create',
            obj=obj,
            data=Mock(**{'get_data_dump.return_value': data})
        )

        assert msg.format() == {
            'customer': 'test-customer',
            'meta': {
                'event_name': 'event.create',
                'obj': {
                    'model': 'ghostdb.core.event.tests.test_message.DataObj',
                    'pk': obj.id.hex,
                },
            },
            'data': data,
        }
