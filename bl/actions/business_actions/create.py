import typing

from ghostdb.db.models import business
from ..utils import base


class BusinessCreate(base.BaseAction):

    def process(self, _business: business.Business) -> typing.Tuple[business.Business, bool]:
        self.db.add(_business)
        self.db.commit()

        return (_business, True)


class ContactCreate(base.BaseAction):

    def process(
        self,
        _business: business.Business,
        contact: business.BusinessContact
    ) -> typing.Tuple[business.BusinessContact, bool]:
        if contact.business != _business or contact.bussiness_id != _business.id:
            contact.business_id = _business.id

        self.db.add(contact)
        self.db.commit()

        return (contact, True)
