import typing

from ghostdb.db.models import business
from ..utils import base


class BusinessDelete(base.BaseAction):

    def process(self, _business: business.Business) -> typing.Tuple[business.Business, bool]:
        self.db.delete(_business)
        self.db.commit()

        return (_business, True)


class ContactDelete(base.BaseAction):

    def process(
        self,
        _business: business.Business,
        contact: business.BusinessContact
    ) -> typing.Tuple[business.BusinessContact, bool]:
        assert contact.business == _business

        self.db.delete(contact)
        self.db.commit()

        return (contact, True)
