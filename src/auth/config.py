import os


class Config:
    # Configure as appropriate
    DATABASE_NAME = os.environ.get(
        'P_DATABASE_NAME', 'DFAccount')
    DB_USERNAME = os.environ.get(
        'P_DB_USER', 'deamFear')

    DB_PASSWORD = os.environ.get(
        'P_DB_USER', 'deamFear%402024')
    DB_TYPE = os.environ.get(
        'P_DB_TYPE', 'postgresql+psycopg2')
    DB_HOST = os.environ.get(
        'P_DB_HOST', 'localhost')

    SQLALCHEMY_DATABASE_URI = DB_TYPE+'://'+DB_USERNAME + \
        ':'+DB_PASSWORD+'@'+DB_HOST+'/'+DATABASE_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', '&gg02)sngr+iw)-fc-6_(r^+x1+%5pno03#&xydts*edby&aas')
    JWT_SECRET_KEY = os.environ.get(
        'JWT_SECRET', 'tv8ZdLOwOw0s7FwvVnNR5Sfr0npttjBgsjLMcKkoYeY')
    ENV = os.environ.get('ENV', 'development')
