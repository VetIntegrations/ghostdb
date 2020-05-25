from sqlalchemy import orm


# global object to point to the DB session for FactoryBoy
Session = orm.scoped_session(orm.sessionmaker())
