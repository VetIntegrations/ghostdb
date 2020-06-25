import typing

from ghostdb.db.models import payment
from ..utils import base
from .generic import KPISelectorGenericFilterMixin


class PMSCOGSTransations(KPISelectorGenericFilterMixin, base.BaseSelector):

    def process(
        self
    ) -> typing.Tuple[typing.Iterable[payment.Payment], bool]:

        query = self.db.query(payment.Payment)

        return (query, True)
