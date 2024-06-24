from sqlalchemy import create_engine
from alembic import context
from sqlalchemy import engine_from_config, pool
import os
from dotenv import load_dotenv
from app.database import Base

# Load .env file
load_dotenv()

# Get the URL from environment variables
db_user = os.getenv('P_DB_USER')
db_pass = os.getenv('P_DB_PASS')
db_host = os.getenv('P_DB_HOST')
db_name = os.getenv('P_DATABASE_NAME')
db_port = os.getenv('P_DB_PORT')

# Construct the SQLALCHEMY_DATABASE_URI
sqlalchemy_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Override the sqlalchemy.url in the Alembic configuration
config = context.config
config.set_main_option('sqlalchemy.url', sqlalchemy_url)

# Other Alembic setup...
target_metadata = Base.metadata


# Load .env file
load_dotenv()

print("DB User:", db_user)  # Debugging output

# More environment variable fetches and print statements as needed...

sqlalchemy_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
print("Database URL:", sqlalchemy_url)  # Debugging output


def run_migrations_online():
    """Run migrations in 'online' mode."""
    engine = create_engine(sqlalchemy_url, poolclass=pool.NullPool)
    connection = engine.connect()

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        url=sqlalchemy_url
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

# Make sure to run Alembic commands to trigger this script
