import uuid
import factory
from datetime import date
from hashlib import sha384

from ghostdb.db.tests import common
from .. import corporation, client, pet, order, business, provider, kpi, payment, user, security


class CorporationFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = corporation.Corporation
        sqlalchemy_session = common.Session

    name = factory.Faker('company')


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = client.Client
        sqlalchemy_session = common.Session

    first_name = factory.Faker('first_name')
    first_name = factory.Faker('last_name')
    email = factory.Faker('email')


class PetFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = pet.Pet
        sqlalchemy_session = common.Session

    name = factory.Faker('first_name')
    registration_date = factory.Faker('date_between', start_date='-10y')
    birthdate = factory.Faker('date_of_birth', minimum_age=1, maximum_age=10)


class BusinessFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = business.Business
        sqlalchemy_session = common.Session

    corporation = factory.SubFactory(CorporationFactory)
    name = factory.Faker('company')
    display_name = factory.SelfAttribute('name')
    timezone = factory.Faker('timezone')


class ProviderFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = provider.Provider
        sqlalchemy_session = common.Session

    business = factory.SubFactory(BusinessFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


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


class InternalKPIValueFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = kpi.InternalKPIValue
        sqlalchemy_session = common.Session

    corporation = factory.SubFactory(CorporationFactory)
    kind = kpi.KPIKind.FINANCIAL_NET_PROFIT
    value = 1
    date = factory.LazyFunction(date.today)


class PaymentFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = payment.Payment
        sqlalchemy_session = common.Session

    corporation = factory.SubFactory(CorporationFactory)
    business = factory.SubFactory(BusinessFactory)
    provider = factory.SubFactory(ProviderFactory)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = user.User
        sqlalchemy_session = common.Session

    id = factory.LazyFunction(uuid.uuid1)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class TemporaryTokenFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = security.TemporaryToken
        sqlalchemy_session = common.Session

    token = factory.Sequence(lambda i: sha384('temporary-token-{}'.format(i).encode('utf-8')).hexdigest())
    user = factory.SubFactory(UserFactory)
