import os
import environ

# Initialize environ
env = environ.Env()
# Reading .env file
environ.Env.read_env()


class Config:
    # Configure as appropriate
    DATABASE_NAME = env('P_DATABASE_NAME', default='DFtext2text')
    DB_USERNAME = env('P_DB_USER', default='DFtext2text')
    DB_PASSWORD = env('P_DB_PASSWORD', default='DFtext2text%402024')
    DB_TYPE = env('P_DB_TYPE', default='postgresql+psycopg2')
    DB_HOST = env('P_DB_HOST', default='localhost')

    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = env(
        'SECRET_KEY', default='7f0299512e1a12bd1f31d90f24e61aa4a555b70a1b09cf1c6ef2d6d0b9049076')
    ENV = env('ENV', default='development')
    OPENAI_KEY = env('OPENAI_SECRET_KEY')

    AUTH_SVC_ADDRESS = "http://127.0.0.1:5000"
