import os


class Config:
    # Configure as appropriate
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://deamFear:deamFear%402024@localhost/DFAccount'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '&gg02)sngr+iw)-fc-6_(r^+x1+%5pno03#&xydts*edby&aas'
    JWT_SECRET_KEY = 'tv8ZdLOwOw0s7FwvVnNR5Sfr0npttjBgsjLMcKkoYeY'
    ENV = 'development'
