import factory

from ghostdb.db.tests import common
from .. import corporation, client, order, business, provider


class CorporationFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = corporation.Corporation
        sqlalchemy_session = common.Session

    name = factory.Sequence(lambda n: "Test Corp %03d" % n)


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = client.Client
        sqlalchemy_session = common.Session

    first_name = factory.Faker('first_name')
    first_name = factory.Faker('last_name')
    email = factory.Faker('email')


class BusinessFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = business.Business
        sqlalchemy_session = common.Session

    corporation = factory.SubFactory(CorporationFactory)
    name = factory.Faker('company')
    display_name = factory.SelfAttribute('name')


class ProviderFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = provider.Provider
        sqlalchemy_session = common.Session

    business = factory.SubFactory(BusinessFactory)
    first_name = factory.Faker('first_name')
    first_name = factory.Faker('last_name')


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = order.Order
        sqlalchemy_session = common.Session

    corporation = factory.SubFactory(CorporationFactory)
    client = factory.SubFactory(ClientFactory)


class OrderItemFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = order.OrderItem
        sqlalchemy_session = common.Session

    order = factory.SubFactory(OrderFactory)
