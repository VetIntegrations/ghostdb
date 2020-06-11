from datetime import datetime
from sqlalchemy import orm

from ghostdb.db.models import order, corporation, business as business_model, kpi as kpi_model
from .utils import base, generic
from .kpi_selectors.revenue import PMSGrossRevenueTransations
from .kpi_selectors.discount import PMSDiscountedTransations
from .kpi_selectors.refund import PMSRefundTransactions
from .kpi_selectors.inventory import PMSInventoryTransations


class KPIValueSelector(base.BaseSelectorSet):

    by_corporation = base.SelectorFactory(
        generic.ByCustomField.factory(filter_field=kpi_model.KPIValue.corporation_id),
        kpi_model.KPIValue
    )
    by_business = base.SelectorFactory(
        generic.ByCustomField.factory(filter_field=kpi_model.KPIValue.business_id),
        kpi_model.KPIValue
    )
    by_provider = base.SelectorFactory(
        generic.ByCustomField.factory(filter_field=kpi_model.KPIValue.provider_id),
        kpi_model.KPIValue
    )


class KPISelector(base.BaseSelectorSet):

    pms_gross_revenue = base.SelectorFactory(PMSGrossRevenueTransations, None)
    pms_discount = base.SelectorFactory(PMSDiscountedTransations, None)
    pms_refunds = base.SelectorFactory(PMSRefundTransactions, None)
    pms_inventory_transactions = base.SelectorFactory(PMSInventoryTransations, None)

    @staticmethod
    def filter_orderitem_by_corporation(
        order_relation: orm.util.AliasedClass,
        query: orm.query.Query,
        corp: corporation.Corporation
    ) -> orm.query.Query:
        return query.filter(
            order_relation.corporation == corp
        )

    @staticmethod
    def filter_orderitem_by_timerange(
        query: orm.query.Query,
        datetime_from: datetime,
        datetime_to: datetime
    ) -> orm.query.Query:
        return query.filter(
            order.OrderItem.created_at >= datetime_from,
            order.OrderItem.created_at < datetime_to,
        )

    @staticmethod
    def filter_orderitem_by_business(
        order_relation: orm.util.AliasedClass,
        query: orm.query.Query,
        business: business_model.Business
    ) -> orm.query.Query:
        return query.filter(
            order_relation.business == business
        )
