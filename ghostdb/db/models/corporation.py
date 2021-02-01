import uuid

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, SmallInteger, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import LtreeType

from .. import meta
from .. import sqltypes


class Corporation(meta.Base):
    __tablename__ = 'corporations'

    id = Column(sqltypes.UUID, default=uuid.uuid1, primary_key=True)
    name = Column(String(200), nullable=True)
    maturity_level = Column(SmallInteger, nullable=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    members = relationship('Member', back_populates='corporation', cascade='all, delete')
    users = relationship('User', back_populates='corporation')

    def __repr__(self):
        return '<Corporation id={} name={}>'.format(self.id, self.name)


class Member(meta.Base):
    __tablename__ = 'members'

    id = Column(sqltypes.UUID, default=uuid.uuid1, primary_key=True)
    user_id = Column(sqltypes.UUID, ForeignKey('users.id'))
    corporation_id = Column(sqltypes.UUID, ForeignKey('corporations.id'))
    invite_id = Column(String(96), ForeignKey('temporary_token.token'))
    role = Column(String(100), nullable=False)
    responsibilities = Column(Text)

    date_of_join = Column(DateTime(timezone=True))
    path = Column(LtreeType)
    ordering = Column(Integer, default=0)

    is_temporary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    corporation = relationship("Corporation", back_populates="members")
    user = relationship("User", back_populates="members")
    invite = relationship("TemporaryToken")
