import typing

from ghostdb.db.models import client
from ..utils import base


class ClientDelete(base.BaseAction):

    def process(self, _client: client.Client) -> typing.Tuple[client.Client, bool]:
        self.db.delete(_client)
        self.db.commit()

        return (_client, True)


class ContactDelete(base.BaseAction):

    def process(
        self,
        _client: client.Client,
        contact: client.ClientContact
    ) -> typing.Tuple[client.ClientContact, bool]:
        assert contact.client == _client

        self.db.delete(contact)
        self.db.commit()

        return (contact, True)


class AddressDelete(base.BaseAction):

    def process(
        self,
        _client: client.Client,
        address: client.ClientAddress
    ) -> typing.Tuple[client.ClientAddress, bool]:
        assert address.client == _client

        self.db.delete(address)
        self.db.commit()

        return (address, True)
