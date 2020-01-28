import typing

from ghostdb.db.models import provider
from ..utils import base


class ProviderDelete(base.BaseAction):

    def process(self, _provider: provider.Provider) -> typing.Tuple[provider.Provider, bool]:
        self.db.delete(_provider)
        self.db.commit()

        return (_provider, True)


class ContactDelete(base.BaseAction):

    def process(
        self,
        _provider: provider.Provider,
        contact: provider.ProviderContact
    ) -> typing.Tuple[provider.ProviderContact, bool]:
        assert contact.provider == _provider

        self.db.delete(contact)
        self.db.commit()

        return (contact, True)
