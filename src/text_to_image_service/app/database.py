from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
db_session = None
engine = None


def init_db(app):
    global db_session
    global engine
    if app:
        engine = create_engine(
            app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
        session_factory = sessionmaker(
            bind=engine, autocommit=False, autoflush=False)
        db_session = scoped_session(session_factory)
        Base.query = db_session.query_property()
        from app import models  # Import all models
        Base.metadata.create_all(bind=engine)


def shutdown_session(exception=None):
    # This function is called when the app context is torn down.
    # Here we commit the session if no exceptions occur, otherwise rollback.
    global db_session
    if db_session:
        if exception is None:
            db_session.commit()
        else:
            db_session.rollback()
        db_session.remove()
