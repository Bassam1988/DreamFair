import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Configure as appropriate
    DATABASE_NAME = os.getenv(
        'P_DATABASE_NAME', 'DFAccount')
    DB_USERNAME = os.getenv(
        'P_DB_USER', 'deamFear')

    DB_PASSWORD = os.getenv(
        'P_DB_PASS', 'deamFear')
    DB_TYPE = os.getenv(
        'P_DB_TYPE', 'postgresql+psycopg2')
    DB_HOST = os.getenv(
        'P_DB_HOST', 'localhost')

    SQLALCHEMY_DATABASE_URI = DB_TYPE+'://'+DB_USERNAME + \
        ':'+DB_PASSWORD+'@'+DB_HOST+'/'+DATABASE_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', '&gg02)sngr+iw')
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET', 'tv8ZdLOwO')
    ENV = os.getenv('ENV', 'development')
