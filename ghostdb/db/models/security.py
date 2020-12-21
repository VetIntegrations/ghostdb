import enum
from sqlalchemy import Column, ForeignKey, String, DateTime, JSON, Enum
from sqlalchemy.orm import relationship

from .. import meta
from .. import sqltypes


class TokenKind(enum.Enum):
    ACCOUNT_DELETION = 'Account deletion'
    EMAIL_VALIDATION = 'Email validation'
    CORPORATION_INVITE = 'Corporation invite'
    PASSWORD_RECOVERY = 'Password recovery'


class TemporaryToken(meta.Base):
    __tablename__ = 'temporary_token'

    token = Column(String(96), primary_key=True)
    kind = Column(Enum(TokenKind))
    expires_at = Column(DateTime)
    user_id = Column(sqltypes.UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    extra = Column(JSON, nullable=True)

    created_at = Column(DateTime, server_default=sqltypes.UTCNow())
    updated_at = Column(DateTime, onupdate=sqltypes.UTCNow())

    user = relationship("user.User")
