import typing

from ghostdb.db.models import client
from ..utils import base


class Create(base.BaseAction):

    def process(self, _client: client.Client) -> typing.Tuple[client.Client, bool]:
        self.db.add(_client)
        self.db.commit()

        return (_client, True)
