class GhostDBException(Exception):
    ...


class NoDefaultDatabase(GhostDBException):
    message = 'Default database session not registered'
