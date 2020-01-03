import uuid
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.dialects.postgresql import UUID as pgUUID


class UUID(TypeDecorator):

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(pgUUID())
        elif dialect.name == 'mysql':
            return dialect.type_descriptor(BINARY(16))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)

            if dialect.name == 'mysql':
                return value.bytes
            else:
                return value.hex  # fine for postgresql

    def process_result_value(self, value, dialect):
        if value is not None:
            if not isinstance(value, uuid.UUID):
                if dialect.name == 'mysql':
                    value = uuid.UUID(bytes=value)
                else:
                    value = uuid.UUID(value)  # fine for postgresql

        return value
