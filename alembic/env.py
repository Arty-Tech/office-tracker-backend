import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. Carica le variabili d’ambiente da “.env”
# -----------------------------------------------------------------------------
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# -----------------------------------------------------------------------------
# 2. Config di Alembic (legge alembic.ini)
# -----------------------------------------------------------------------------
config = context.config

# -----------------------------------------------------------------------------
# 3. Sovrascrivi “sqlalchemy.url” con DATABASE_URL dal .env,
#    ma *rimuoviamo* “+asyncpg” per far usare il driver sincrono
# -----------------------------------------------------------------------------
database_url = os.getenv("DATABASE_URL")
if database_url:
    sync_database_url = database_url.replace("+asyncpg", "")
    config.set_main_option("sqlalchemy.url", sync_database_url)

# -----------------------------------------------------------------------------
# 4. Configura il logging tramite il file alembic.ini
# -----------------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------------------------------------------------------
# 5. Importa Base e tutti i modelli “sotto” perché Alembic
#    conosca tutte le tabelle (target_metadata = Base.metadata).
# -----------------------------------------------------------------------------
from app.db.base import Base
from app.models.user import User
from app.models.workday_config import WorkDayConfig
from app.models.punch import Punch
from app.models.time_entry import TimeEntry  # <-- IMPORT CORRETTO
# ... importa eventuali altri modelli che hai (TimeEntry, …)

target_metadata = Base.metadata

# -----------------------------------------------------------------------------
# 6. Funzioni per offline/online migrations
# -----------------------------------------------------------------------------
def run_migrations_offline():
    """Migrations in “offline” mode: genera SQL senza connessione diretta."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Migrations in “online” mode: apre una connessione sincrona."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------------------------------------------------------
# 7. Esecuzione della migration in base alla modalità
# -----------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
