from sqlmodel import Session
from sqlalchemy import create_engine

class DatabaseManager:
    engine = None

    def __init__(self, database_url: str):
        DatabaseManager.engine = create_engine(database_url, echo=True, pool_pre_ping=True)

    @staticmethod
    def get_session():
        with Session(DatabaseManager.engine) as session:
            yield session
