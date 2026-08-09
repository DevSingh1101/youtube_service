from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    username: str = Field(index=True, unique=True)
    hashed_password: str = Field()
