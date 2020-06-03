import typing

from ghostdb.db.models import client
from ..utils import base


class ByEmail(base.BaseSelector):

    def process(self, email: str) -> typing.Tuple[client.Client, bool]:
        query = (
            self.db.query(client.Client)
            .filter(client.Client.email == email)
        )

        _client = query.first()

        return (_client, _client is not None)
