from .utils import base
from .kpi_selectors.revenue import PMSGrossRevenueTransations
from .kpi_selectors.discount import PMSDiscountedTransations


class KPISelector(base.BaseSelectorSet):

    pms_gross_revenue = base.SelectorFactory(PMSGrossRevenueTransations, None)
    pms_discount = base.SelectorFactory(PMSDiscountedTransations, None)
