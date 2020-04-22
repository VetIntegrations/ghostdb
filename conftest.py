import os
import warnings
import pytest
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, session

from ghostdb.db import meta
from ghostdb.core.event import event


class MockDB:

    def __init__(self):
        self.log = []

    def __getattr__(self, name):
        def mock_method(*args, **kwargs):
            self.log.append((name, args, kwargs))

        return mock_method


@pytest.fixture
def mock_default_database():
    db = MockDB()

    meta.register_dbsession('default', db)
    yield db

    del meta.DATABASES['default']


@pytest.fixture(scope='session')
def db_connection():
    engine = create_engine(os.environ['GHOSTDB_DB_DSN'])
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='session', autouse=True)
def db_structure(db_connection):
    meta.initialize()

    meta.Base.metadata.create_all(bind=db_connection)
    yield
    meta.Base.metadata.drop_all(bind=db_connection)


@pytest.fixture
def dbsession(db_connection):
    transaction = db_connection.begin()
    db = Session(bind=db_connection, autocommit=False)

    yield db

    transaction.rollback()
    session.close_all_sessions()


@pytest.fixture(scope='function')
def default_database(db_connection):
    warnings.warn("migrate to dbsession", DeprecationWarning)

    transaction = db_connection.begin()
    db = Session(bind=db_connection, autocommit=False)
    meta.register_dbsession('default', db)

    yield db

    transaction.rollback()
    session.close_all_sessions()
    del meta.DATABASES['default']


@pytest.fixture(scope='function')
def event_off(monkeypatch):
    event_mock = Mock()
    monkeypatch.setattr(event.InternalEvent, 'trigger', event_mock)

    yield event_mock
