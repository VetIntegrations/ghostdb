import uuid

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .. import meta, sqltypes


class User(meta.Base):
    __tablename__ = 'users'

    id = Column(sqltypes.UUID, default=uuid.uuid1, primary_key=True)
    password = Column(String(128))
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    is_ghost = Column(Boolean, default=True)  # not validated user

    salt = Column(String(32))
    last_changed_password = Column(DateTime(timezone=True))
    last_visited = Column(DateTime(timezone=True))

    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), nullable=True)
    date_of_join = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=False)  # user that doesn't accept invite to the corporation

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    members = relationship("Member", back_populates="user")
