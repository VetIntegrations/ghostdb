import typing

from ghostdb.db.models import provider
from ..utils import base


class ProviderCreate(base.BaseAction):

    def process(self, _provider: provider.Provider) -> typing.Tuple[provider.Provider, bool]:
        self.db.add(_provider)
        self.db.commit()

        return (_provider, True)


class ContactCreate(base.BaseAction):

    def process(
        self,
        contact: provider.ProviderContact,
        _provider: provider.Provider
    ) -> typing.Tuple[provider.ProviderContact, bool]:
        if contact.provider != _provider or contact.provider_id != _provider.id:
            contact.provider_id = _provider.id

        self.db.add(contact)
        self.db.commit()

        return (contact, True)
