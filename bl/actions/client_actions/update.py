import typing

from ghostdb.db.models import client
from ..utils import base


class ClientUpdate(base.BaseAction):

    def process(self, _client: client.Client) -> typing.Tuple[client.Client, bool]:
        self.db.add(_client)
        self.db.commit()

        return (_client, True)


class ContactUpdate(base.BaseAction):

    def process(
        self,
        _client: client.Client,
        contact: client.ClientContact
    ) -> typing.Tuple[client.ClientContact, bool]:
        assert contact.client == _client

        self.db.add(contact)
        self.db.commit()

        return (contact, True)


class AddressUpdate(base.BaseAction):

    def process(
        self,
        _client: client.Client,
        address: client.ClientAddress
    ) -> typing.Tuple[client.ClientAddress, bool]:
        assert address.client == _client

        self.db.add(address)
        self.db.commit()

        return (address, True)
