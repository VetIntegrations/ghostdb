import enum
import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, Boolean, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from .. import meta
from .. import sqltypes


class RevenueCenter(meta.Base):
    __tablename__ = 'glcode_revenuecenter'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<RevenueCenter name={}>'.format(self.name)


class Department(meta.Base):
    __tablename__ = 'glcode_department'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Department name={}>'.format(self.name)


class Category(meta.Base):
    __tablename__ = 'glcode_category'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Department name={}>'.format(self.name)


class Class(meta.Base):
    __tablename__ = 'glcode_class'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<Class name={}>'.format(self.name)


class SubClass(meta.Base):
    __tablename__ = 'glcode_subclass'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<SubClass name={}>'.format(self.name)


class ServiceType(meta.Base):
    __tablename__ = 'glcode_servicetype'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    is_vis_default = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return '<ServiceType name={}>'.format(self.name)


class ServiceKind(enum.Enum):
    service = 'Service'
    product = 'Product'
    inventory = 'Inventory'
    admin = 'Admin.'


class Service(meta.Base):
    __tablename__ = 'glcode_service'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    kind = Column(Enum(ServiceKind), nullable=False)
    revenue_center_id = Column(sqltypes.UUID, ForeignKey('glcode_revenuecenter.id'))
    department_id = Column(sqltypes.UUID, ForeignKey('glcode_department.id'))
    category_id = Column(sqltypes.UUID, ForeignKey('glcode_category.id'))
    class_id = Column(sqltypes.UUID, ForeignKey('glcode_class.id'))
    subclass_id = Column(sqltypes.UUID, ForeignKey('glcode_subclass.id'))
    servicetype_id = Column(sqltypes.UUID, ForeignKey('glcode_servicetype.id'))
    is_vis_default = Column(Boolean, default=False)
    pms_ids = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    revenue_center = relationship('RevenueCenter', backref=backref('services'))
    department = relationship('Department', backref=backref('services'))
    category = relationship('Category', backref=backref('services'))
    klass = relationship('Class', backref=backref('services'))
    subclass = relationship('SubClass', backref=backref('services'))
    service_type = relationship('ServiceType', backref=backref('services'))

    def __repr__(self):
        return '<Service name={}>'.format(self.name)
