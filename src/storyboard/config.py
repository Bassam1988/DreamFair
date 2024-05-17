import os


class Config:
    # Configure as appropriate
    DATABASE_NAME = os.environ.get(
        'P_DATABASE_NAME', 'storyboard')
    DB_USERNAME = os.environ.get(
        'P_DB_USER', 'storyboard')

    DB_PASSWORD = os.environ.get(
        'P_DB_USER', 'storyboard%402024')
    DB_TYPE = os.environ.get(
        'P_DB_TYPE', 'postgresql+psycopg2')
    DB_HOST = os.environ.get(
        'P_DB_HOST', 'localhost')

    SQLALCHEMY_DATABASE_URI = DB_TYPE+'://'+DB_USERNAME + \
        ':'+DB_PASSWORD+'@'+DB_HOST+'/'+DATABASE_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'f6f2c03a2231bc619208c65fdf87efc9fd1053d41f096e141de494c741a5658e')
    # JWT_SECRET_KEY = os.environ.get(
    #     'JWT_SECRET', 'VvbXl2qZBhRY6s3b1S+HKJuZFJoGuq9tkD23gY609Qo')
    ENV = os.environ.get('ENV', 'development')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTH_SVC_ADDRESS = "http://127.0.0.1:5000"
