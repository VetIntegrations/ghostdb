import enum
import uuid

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, JSON, Enum, DateTime
)
from sqlalchemy.orm import relationship

from .. import meta
from .. import sqltypes


class Corporation(meta.Base):
    __tablename__ = 'corporations'

    id = Column(sqltypes.UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    integrations = relationship('Integration', back_populates='corporation')
    users = relationship("User", back_populates="corporation")

    def __repr__(self):
        return '<Corporation id={} name={}>'.format(self.id, self.name)


class IntegrationModules(enum.Enum):
    vetsuccess = 'VetSuccess'


class Integration(meta.Base):
    __tablename__ = 'corporation_integrations'

    id = Column(Integer, primary_key=True)
    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=False)
    name = Column(String(100), nullable=False)
    module = Column(Enum(IntegrationModules), nullable=False)
    auth_credentials = Column(JSON)
    is_enable = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    corporation = relationship("Corporation", back_populates="integrations")

    def __repr__(self):
        return '<Integration id={} corporation={} name={}>'.format(
            self.id,
            self.corporation.name,
            self.name
        )
