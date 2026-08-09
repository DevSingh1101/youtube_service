from sqlalchemy import create_engine
from sqlmodel import Session

class DatabaseManager:
    engine = None

    def __init__(self):
        DatabaseManager.engine = create_engine(f"sqlite:///database.db")

    @staticmethod
    def get_session():
        with Session(DatabaseManager.engine) as session:
            yield session
