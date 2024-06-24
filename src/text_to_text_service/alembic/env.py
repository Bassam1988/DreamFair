from app.models import *  # Adjust the import path to your models module
from app.database import Base
from sqlalchemy import engine_from_config, pool
from alembic import context
from logging.config import fileConfig
import sys
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Debug print to check environment variables
print("Loading environment variables...")
db_user = os.getenv('P_DB_USER')
db_pass = os.getenv('P_DB_PASS')
db_host = os.getenv('P_DB_HOST')
db_name = os.getenv('P_DATABASE_NAME')
db_port = os.getenv('P_DB_PORT')
sqlalchemy_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# It's important to import your models here, so Alembic can access the Base.metadata
sys.path.append(os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', sqlalchemy_url)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add metadata
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        dialect_opts={"paramstyle": 'named'}
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata  # Ensure metadata is passed here
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
