from dotenv import load_dotenv
import os

# Initialize environ
load_dotenv()


class Config:
    # Configure as appropriate
    DATABASE_NAME = os.getenv('P_DATABASE_NAME')
    DB_USERNAME = os.getenv('P_DB_USER')
    DB_PASSWORD = os.getenv('P_DB_PASSWORD')
    DB_TYPE = os.getenv('P_DB_TYPE')
    DB_HOST = os.getenv('P_DB_HOST', default='localhost')

    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='960000341d39eeda6fc7586')
    ENV = os.getenv('ENV', default='development')
    OPENAI_KEY = os.getenv('OPENAI_SECRET_KEY')

    AUTH_SVC_ADDRESS = "http://127.0.0.1:5000"

    MONGODB_URI = os.getenv(
        'MONGODB_URI', default='mongodb://127.0.0.1:27017/t2m_images')
