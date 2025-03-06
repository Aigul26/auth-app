import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from abc import ABC, abstractmethod
from app.config.config import settings

class DatabaseConnection(ABC):
    @abstractmethod
    def get_engine(self) -> AsyncEngine:
        """Создать и вернуть асинхронный движок SQLAlchemy"""
        pass

    @abstractmethod
    def get_sessionmaker(self):
        """Создать и вернуть асинхронную фабрику сессий"""
        pass


class PostgresConnection(DatabaseConnection):
    def __init__(self, database_url: str):
        self.database_url = database_url

    def get_engine(self) -> AsyncEngine:
        return create_async_engine(self.database_url)

    def get_sessionmaker(self):
        return async_sessionmaker(bind=self.get_engine(), expire_on_commit=False)
    

class MySQLConnection(DatabaseConnection):
    def __init__(self, database_url: str):
        self.database_url = database_url

    def get_engine(self) -> AsyncEngine:
        return create_async_engine(self.database_url)

    def get_sessionmaker(self):
        return async_sessionmaker(bind=self.get_engine(), expire_on_commit=False)
    

def get_database_connection(database_url: str, db_type: str) -> DatabaseConnection:
    if db_type == "postgres":
        return PostgresConnection(database_url)
    elif db_type == "mysql":
        return MySQLConnection(database_url)

    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f'Database URL: {settings.database_url}')

db_type = "postgres"
db_connection = get_database_connection(settings.database_url, db_type)
    
engine = db_connection.get_engine()
async_session_maker = db_connection.get_sessionmaker()

logger.info(f"Connected to {db_type} database at {settings.database_url}")