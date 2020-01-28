import typing

from ghostdb.db.models import provider
from ..utils import base


class ProviderUpdate(base.BaseAction):

    def process(self, _provider: provider.Provider) -> typing.Tuple[provider.Provider, bool]:
        self.db.add(_provider)
        self.db.commit()

        return (_provider, True)


class ContactUpdate(base.BaseAction):

    def process(
        self,
        _provider: provider.Provider,
        contact: provider.ProviderContact
    ) -> typing.Tuple[provider.ProviderContact, bool]:
        assert contact.provider == _provider

        self.db.add(contact)
        self.db.commit()

        return (contact, True)
