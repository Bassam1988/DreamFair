from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

Base = declarative_base()
db_session = None
engine = None


def init_db(app):
    global db_session
    global engine
    if app:
        db_name = os.getenv('P_DATABASE_NAME')
        db_user = os.getenv('P_DB_USER')

        db_password = os.getenv('P_DB_PASS')
        db_type = os.getenv('P_DB_TYPE')
        db_host = os.getenv('P_DB_HOST')

        db_uri = db_type+'://'+db_user + \
            ':'+db_password+'@'+db_host+'/'+db_name
        engine = create_engine(db_uri, echo=True)
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


def init_consumer_db():
    db_name = os.getenv('P_DATABASE_NAME')
    db_user = os.getenv('P_DB_USER')

    db_password = os.getenv('P_DB_PASS')
    db_type = os.getenv('P_DB_TYPE')
    db_host = os.getenv('P_DB_HOST')

    db_uri = db_type+'://'+db_user + \
        ':'+db_password+'@'+db_host+'/'+db_name
    engine = create_engine(db_uri, echo=True)
    # Update with your actual DB URI
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)  # Create tables if they don't exist
    return scoped_session(SessionLocal)
