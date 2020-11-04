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
        contact: client.ClientContact,
        _client: client.Client
    ) -> typing.Tuple[client.ClientContact, bool]:
        contact.client = _client

        self.db.delete(contact)
        self.db.commit()

        return (contact, True)


class AddressDelete(base.BaseAction):

    def process(
        self,
        address: client.ClientAddress,
        _client: client.Client
    ) -> typing.Tuple[client.ClientAddress, bool]:
        if address.client != _client:
            raise ValueError(f'addres should belongs to "{_client}" client')

        self.db.delete(address)
        self.db.commit()

        return (address, True)
