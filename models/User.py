import re

from pydantic import field_validator
from sqlmodel import Field, SQLModel

ALLOWED_EMAIL_DOMAINS = {"domain.com", "gmail.com", "yahoo.com", "outlook.com"}

class UserBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(index=True, unique=True, max_length=50)

    @field_validator("email")
    def validate_email(cls, email_str: str) -> str:
        if not re.fullmatch(r"^[\w.+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})$", email_str):
            raise ValueError("Invalid email format, Please provide a valid email address")

        domain = email_str.rsplit("@", 1)[1].lower()
        if domain not in ALLOWED_EMAIL_DOMAINS:
            allowed = ", ".join(sorted(ALLOWED_EMAIL_DOMAINS))
            raise ValueError(f"Email domain must be one of: {allowed}")

        return email_str.lower()


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=8)
