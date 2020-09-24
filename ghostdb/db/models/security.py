from sqlalchemy import Column, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship

from .. import meta
from .. import sqltypes


class TemporaryToken(meta.Base):
    __tablename__ = 'temporary_token'

    token = Column(String(96), primary_key=True)
    expires_at = Column(DateTime)
    user_id = Column(sqltypes.UUID, ForeignKey('users.id'), nullable=True)
    extra = Column(JSON, nullable=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    user = relationship("user.User")
