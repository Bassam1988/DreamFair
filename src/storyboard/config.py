from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    # Configure as appropriate
    DATABASE_NAME = os.getenv(
        'P_DATABASE_NAME', 'storyboard')
    DB_USERNAME = os.getenv(
        'P_DB_USER', 'storyboard')

    DB_PASSWORD = os.getenv(
        'P_DB_USER', 'storyboard')
    DB_TYPE = os.getenv(
        'P_DB_TYPE', 'postgresql+psycopg2')
    DB_HOST = os.getenv(
        'P_DB_HOST', 'localhost')

    SQLALCHEMY_DATABASE_URI = DB_TYPE+'://'+DB_USERNAME + \
        ':'+DB_PASSWORD+'@'+DB_HOST+'/'+DATABASE_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', 'f6f2c03a2231bc')
    # JWT_SECRET_KEY = os.environ.get(
    #     'JWT_SECRET', 'VvbXl2qZBhRY6s3b1S+HKJuZFJoGuq9tkD23gY609Qo')
    ENV = os.getenv('ENV', 'development')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTH_SVC_ADDRESS = os.getenv('AUTH_SVC_ADDRESS')
