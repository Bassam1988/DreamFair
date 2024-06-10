from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    # Configure as appropriate
    DATABASE_NAME = os.getenv('P_DATABASE_NAME')
    DB_USERNAME = os.getenv('P_DB_USER')
    DB_PASSWORD = os.getenv('P_DB_PASSWORD')
    DB_TYPE = os.getenv('P_DB_TYPE', default='postgresql+psycopg2')
    DB_HOST = os.getenv('P_DB_HOST', default='localhost')

    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='7f0299512e1a12bd1f')
    ENV = os.getenv('ENV', default='development')
    OPENAI_KEY = os.getenv('OPENAI_SECRET_KEY')

    AUTH_SVC_ADDRESS = os.getenv("AUTH_SVC_ADDRESS")
