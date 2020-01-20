import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, session

from ghostdb.db import meta


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


@pytest.fixture(scope='function')
def default_database(db_connection):
    transaction = db_connection.begin()
    db = Session(bind=db_connection, autocommit=False)
    meta.register_dbsession('default', db)

    yield db

    transaction.rollback()
    # db.close_all()
    session.close_all_sessions()
    del meta.DATABASES['default']
