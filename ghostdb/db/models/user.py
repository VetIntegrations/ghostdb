import uuid

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .. import meta, sqltypes


class User(meta.Base):
    __tablename__ = 'users'

    id = Column(sqltypes.UUID, default=uuid.uuid1, primary_key=True)
    username = Column(String(50))
    password = Column(String(128))
    email = Column(String(100))
    first_name = Column(String(200))
    last_name = Column(String(200))
    is_active = Column(Boolean, default=True)

    salt = Column(String(32))
    last_changed_password = Column(DateTime(timezone=True))
    last_visited = Column(DateTime(timezone=True))

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    members = relationship("Member", back_populates="user")


class Member(meta.Base):
    __tablename__ = 'members'

    user_id = Column(sqltypes.UUID, ForeignKey('users.id'), primary_key=True)
    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'), primary_key=True)

    date_of_join = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="members")
    corporation = relationship("Corporation", back_populates="members")
