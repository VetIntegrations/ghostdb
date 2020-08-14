from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from ghostdb.db.meta import Base, initialize
from ghostdb.db.models.appointment import AppointmentKind, AppointmentSource, Appointment
from ghostdb.db.models.corporation import Corporation, Integration
from ghostdb.db.models.pet import (
    Breed, Color, Gender, Species, WeightUnit, Pet, PetOwner
)
from ghostdb.db.models.client import Client, ClientAddress, ClientContact
from ghostdb.db.models.business import Business, BusinessContact
from ghostdb.db.models.provider import ProviderKind, Provider, ProviderContact
from ghostdb.db.models.code import (
    Category, Class, Department, RevenueCenter,
    ServiceType, SubClass, Service
)
from ghostdb.db.models.kpi import KPIValue
from ghostdb.db.models.order import Order, OrderItem
from ghostdb.db.models.payment import Payment


def migrate():

    models = [
        AppointmentKind,
        AppointmentSource,
        Breed,
        Client,
        Color,
        Corporation,
        Gender,
        Category,
        Class,
        Department,
        RevenueCenter,
        ServiceType,
        SubClass,
        ProviderKind,
        Species,
        WeightUnit,
        Business,
        ClientAddress,
        ClientContact,
        Integration,
        Pet,
        BusinessContact,
        Service,
        PetOwner,
        Provider,
        Appointment,
        # KPIValue,
        Order,
        Payment,
        ProviderContact,
        OrderItem
    ]

    initialize()

    engine_mysql = create_engine('mysql://vis:vis@127.0.0.1:13306/vis')
    engine_pg = create_engine('postgresql://postgres:vis@localhost:5432/vis')

    Base.metadata.create_all(bind=engine_mysql)
    Base.metadata.create_all(bind=engine_pg)

    session_mysql = Session(bind=engine_mysql)
    session_pg = Session(bind=engine_pg)

    for model in models:
        count_items = session_mysql.query(model).count()

        print(f'{datetime.now()} :: START datamigration, model: {model}, items: {count_items}')
        i = 0
        offset = 0
        limit = 1000

        while True:
            for item in session_mysql.query(model).offset(offset).limit(limit):
                local_item = session_pg.merge(item)
                session_pg.add(local_item)
                i += 1

            offset += limit

            session_pg.commit()
            print(f'{datetime.now()} :: datamigration, model: {model}, items: {i}/{count_items}')

            if i >= count_items:
                break

        count_items_pg = session_pg.query(model).count()
        print(f'{datetime.now()} :: FINISH, model: {model}, items: {count_items}, pg_items: {count_items_pg}')


if __name__ == '__main__':
    migrate()
