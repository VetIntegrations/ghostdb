import os
from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.schema import MetaData
from sqlalchemy.sql.elements import _defer_none_name
from sqlalchemy.ext.declarative import declarative_base


DATABASES = {}


def ghost_constraint_name(constraint, table):
    """Boolean field doens't generate constraint name.
    """
    if isinstance(constraint.name, (type(None), _defer_none_name)):
        column_names = [
            column.name
            for column in constraint.columns
        ]
        name = '_'.join(column_names)
    else:
        name = constraint.name

    return name


convention = {
    'ghost_constraint_name': ghost_constraint_name,
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(ghost_constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}


Base = declarative_base(
    metadata=MetaData(naming_convention=convention)
)


def initialize():
    models_path = os.path.join(
        os.path.dirname(__file__),
        'models'
    )
    for fl_name in os.listdir(models_path):
        if fl_name.endswith('.py') and not fl_name.startswith('__'):
            import_module('ghostdb.db.models.{}'.format(fl_name[:-3]))


def create_dbsession(uri: str) -> session.Session:
    engine = create_engine(uri)
    db = sessionmaker(bind=engine)

    return db()


def register_dbsession(name: str, db: session.Session):
    DATABASES[name] = db
