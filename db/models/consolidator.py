import enum
import uuid
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, JSON, Enum, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .. import meta
from .. import sqltypes


class Consolidator(meta.Base):
    __tablename__ = 'consolidators'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    integrations = relationship('Integration', back_populates='consolidator')

    def __repr__(self):
        return '<Consolidator(id={} name={})>'.format(self.id, self.name)


class IntegrationModules(enum.Enum):
    vetsuccess = 'VetSuccess'


class Integration(meta.Base):
    __tablename__ = 'consolidator_integrations'

    id = Column(Integer, primary_key=True)
    consolidator_id = Column(sqltypes.UUID, ForeignKey('consolidators.id'))
    name = Column(String(100))
    module = Column(Enum(IntegrationModules))
    auth_credentials = Column(JSON)
    is_enable = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    consolidator = relationship("Consolidator", back_populates="integrations")

    def __repr__(self):
        return '<Integration(id={} consolidator={} name={})>'.format(
            self.id,
            self.consolidator.name,
            self.name
        )
