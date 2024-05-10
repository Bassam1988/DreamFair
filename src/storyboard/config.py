import os


class Config:
    # Configure as appropriate
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://storyboard:storyboard%402024@localhost/storyboard'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'f6f2c03a2231bc619208c65fdf87efc9fd1053d41f096e141de494c741a5658e'
    JWT_SECRET_KEY = 'VvbXl2qZBhRY6s3b1S+HKJuZFJoGuq9tkD23gY609Qo'

    AUTH_SVC_ADDRESS = "http://127.0.0.1:5000"

    ENV = 'development'
