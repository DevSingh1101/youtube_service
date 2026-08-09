from datetime import timedelta, datetime, timezone

from pwdlib import PasswordHash

import jwt

class AuthManager:
    password_hash = None

    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    @staticmethod
    def create_access_token(user_id: str, expires_at:timedelta) -> str:
        now = datetime.now(timezone.utc)

        return jwt.encode(
            {
                "user_id": user_id,
                "exp": now + expires_at,
                "iat": now,
                "type": "access_token",
            },
            "abc",
            "HS256"
        )