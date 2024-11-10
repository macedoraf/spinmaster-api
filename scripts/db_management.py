import logging
import os
import time
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db(db_params: dict, max_retries: int = 30, retry_interval: int = 2) -> bool:
    """Wait for database to become available"""
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**db_params)
            conn.close()
            logger.info("Database is available")
            return True
        except psycopg2.OperationalError:
            if attempt < max_retries - 1:
                logger.info(f"Waiting for database... attempt {attempt + 1}/{max_retries}")
                time.sleep(retry_interval)
            else:
                logger.error("Could not connect to database after maximum retries")
                return False
    return False

def ensure_database_exists(params: dict) -> bool:
    """Ensure database exists, create if it doesn't"""
    try:
        # Conectar ao postgres para criar banco se necessário
        conn_params = params.copy()
        conn_params['database'] = 'postgres'
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar se o banco existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{params['database']}'")
        exists = cursor.fetchone()
        
        if not exists:
            logger.info(f"Creating database {params['database']}")
            cursor.execute(f"CREATE DATABASE {params['database']}")
            logger.info(f"Database {params['database']} created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error ensuring database exists: {e}")
        return False

def run_migrations(database_url: str) -> bool:
    """Run database migrations using Alembic"""
    try:
        logger.info("Running database migrations")
        config = Config("alembic.ini")
        
        # Sobrescrever a URL do banco de dados
        config.set_main_option("sqlalchemy.url", database_url)
        
        # Executar migrações
        command.upgrade(config, "head")
        logger.info("Database migrations completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False

def main():
    # Parâmetros do banco de dados
    db_params = {
        'host': os.getenv('POSTGRES_SERVER', 'postgres'),
        'user': os.getenv('POSTGRES_USER', 'spinmaster'),
        'password': os.getenv('POSTGRES_PASSWORD', 'spinmaster'),
        'database': os.getenv('POSTGRES_DB', 'spinmaster'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }
    
    database_url = (f"postgresql://{db_params['user']}:{db_params['password']}"
                   f"@{db_params['host']}:{db_params['port']}/{db_params['database']}")

    # Esperar pelo PostgreSQL
    if not wait_for_db(db_params):
        logger.error("Could not connect to database. Exiting.")
        exit(1)

    # Garantir que o banco existe
    if not ensure_database_exists(db_params):
        logger.error("Could not ensure database exists. Exiting.")
        exit(1)

    # Executar migrações
    if not run_migrations(database_url):
        logger.error("Could not run migrations. Exiting.")
        exit(1)

    logger.info("Database setup completed successfully")

if __name__ == "__main__":
    main()