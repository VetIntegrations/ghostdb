import enum
import uuid

from sqlalchemy import (
    Column, String, ForeignKey, DateTime, JSON, Boolean, Enum, Table, Numeric
)
from sqlalchemy.orm import relationship, backref

from .. import meta
from .. import sqltypes


class RevenueCenter(meta.Base):
    __tablename__ = 'glcode_revenuecenter'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<RevenueCenter name={}>'.format(self.name)


class Department(meta.Base):
    __tablename__ = 'glcode_department'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Department name={}>'.format(self.name)


class Category(meta.Base):
    __tablename__ = 'glcode_category'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Category name={}>'.format(self.name)


class Class(meta.Base):
    __tablename__ = 'glcode_class'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<Class name={}>'.format(self.name)


class SubClass(meta.Base):
    __tablename__ = 'glcode_subclass'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<SubClass name={}>'.format(self.name)


class ServiceType(meta.Base):
    __tablename__ = 'glcode_servicetype'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    def __repr__(self):
        return '<ServiceType name={}>'.format(self.name)


subclass_rel_table = Table(
    'glcode_srv_subclass_rel',
    meta.Base.metadata,
    Column('subclass', sqltypes.UUID, ForeignKey('glcode_subclass.id')),
    Column('service', sqltypes.UUID, ForeignKey('glcode_service.id'))
)


servicetype_rel_table = Table(
    'glcode_srv_servicetype_rel',
    meta.Base.metadata,
    Column('service_type', sqltypes.UUID, ForeignKey('glcode_servicetype.id')),
    Column('service', sqltypes.UUID, ForeignKey('glcode_service.id'))
)


class ServiceKind(enum.Enum):
    SERVICE = 'Service'
    PRODUCT = 'Product'
    INVENTORY = 'Inventory'
    ADMIN = 'Admin'

    GROUPITEM = 'GroupItem'
    DISCOUNT = 'Discount'
    MEDICAL = 'Medical'
    DIAGNOSTIC = 'Diagnostic'
    SALES_TAX = 'Sales Tax'
    PROBLEM = 'Problem'
    PAYMENT = 'Payment'
    TYPE = 'Type'


class Service(meta.Base):
    __tablename__ = 'glcode_service'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    business_id = Column(sqltypes.UUID, ForeignKey('businesses.id'))
    name = Column(String(200), nullable=False)
    category_description = Column(String(200))
    kind = Column(Enum(ServiceKind))
    revenue_center_id = Column(sqltypes.UUID, ForeignKey('glcode_revenuecenter.id'))
    department_id = Column(sqltypes.UUID, ForeignKey('glcode_department.id'))
    category_id = Column(sqltypes.UUID, ForeignKey('glcode_category.id'))
    class_id = Column(sqltypes.UUID, ForeignKey('glcode_class.id'))
    is_vis_default = Column(Boolean, default=False)
    base_price = Column(Numeric)
    dispensing_fee = Column(Numeric)
    paid_doses = Column(Numeric)  # int or float
    free_doses = Column(Numeric)  # int or float
    unit_of_measure = Column(String(50))
    active = Column(Boolean)
    verified = Column(Boolean)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    revenue_center = relationship('RevenueCenter', backref=backref('services'))
    department = relationship('Department', backref=backref('services'))
    category = relationship('Category', backref=backref('services'))
    klass = relationship('Class', backref=backref('services'))
    subclass = relationship('SubClass', secondary=subclass_rel_table, backref=backref('services'))
    service_type = relationship('ServiceType', secondary=servicetype_rel_table, backref=backref('services'))
    business = relationship('Business', backref=backref('glcode_services'))

    def __repr__(self):
        return '<Service name={}>'.format(self.name)
