import enum
import uuid
from sqlalchemy import (
    Column, ForeignKey, DateTime, JSON, Boolean, Enum, Text, Date, Numeric
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from .. import meta
from .. import sqltypes


class OrderStatus(enum.Enum):
    collections = 'Collections'
    deleted = 'Deleted'
    due = 'Due'
    open = 'Open'
    paid = 'Paid'
    uncollectible = 'Uncollectible'
    void = 'Void'


class Order(meta.Base):
    __tablename__ = 'orders'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=False)
    client_id = Column(sqltypes.UUID, ForeignKey('clients.id'), nullable=False)
    pet_id = Column(sqltypes.UUID, ForeignKey('pets.id'), nullable=False)
    provider_id = Column(sqltypes.UUID, ForeignKey('providers.id'), nullable=False)
    invoice_date = Column(DateTime)
    is_posted = Column(Boolean)
    note = Column(Text)
    status = Column(Enum(OrderStatus))
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    corporation = relationship('Corporation', backref=backref('orders'))
    client = relationship('Client', backref=backref('orders'))
    pet = relationship('Pet', backref=backref('orders'))
    provider = relationship('Provider', backref=backref('orders'))


class OrderItem(meta.Base):
    __tablename__ = 'order_items'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    order_id = Column(sqltypes.UUID, ForeignKey('orders.id'), nullable=False)
    date = Column(Date)
    revenue_center_id = Column(sqltypes.UUID, ForeignKey('glcode_revenuecenter.id'))
    department_id = Column(sqltypes.UUID, ForeignKey('glcode_department.id'))
    category_id = Column(sqltypes.UUID, ForeignKey('glcode_category.id'))
    class_id = Column(sqltypes.UUID, ForeignKey('glcode_class.id'))
    subclass_id = Column(sqltypes.UUID, ForeignKey('glcode_subclass.id'))
    servicetype_id = Column(sqltypes.UUID, ForeignKey('glcode_servicetype.id'))
    service_id = Column(sqltypes.UUID, ForeignKey('glcode_service.id'))
    quantity = Column(Numeric)
    unit_price = Column(Numeric)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    order = relationship('Order', backref=backref('items'))
    revenue_center = relationship('RevenueCenter', backref=backref('order_items'))
    department = relationship('Department', backref=backref('order_items'))
    category = relationship('Category', backref=backref('order_items'))
    klass = relationship('Class', backref=backref('order_items'))
    subclass = relationship('SubClass', backref=backref('order_items'))
    service_type = relationship('ServiceType', backref=backref('order_items'))
    service = relationship('Service', backref=backref('order_items'))
