import typing

from ghostdb.db.models import client
from ..utils import base


class ClientCreate(base.BaseAction):

    def process(self, _client: client.Client) -> typing.Tuple[client.Client, bool]:
        self.db.add(_client)
        self.db.commit()

        return (_client, True)


class ContactCreate(base.BaseAction):

    def process(
        self,
        _client: client.Client,
        contact: client.ClientContact
    ) -> typing.Tuple[client.ClientContact, bool]:
        if contact.client != _client or contact.client_id != _client.id:
            contact.client_id = _client.id

        self.db.add(contact)
        self.db.commit()

        return (contact, True)


class AddressCreate(base.BaseAction):

    def process(
        self,
        _client: client.Client,
        address: client.ClientAddress
    ) -> typing.Tuple[client.ClientAddress, bool]:
        if address.client != _client or address.client_id != _client.id:
            address.client_id = _client.id

        self.db.add(address)
        self.db.commit()

        return (address, True)
