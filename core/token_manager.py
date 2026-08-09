import jwt
from datetime import timedelta, datetime, timezone

class TokenManager:
    secret_key = None
    encoding_algorithm = None

    def __init__(self, secret_key: str, encoding_algorithm: str):
        self.secret_key = secret_key
        self.encoding_algorithm = encoding_algorithm

    def create_access_token(self, user_id: str, username: str, expires_at: timedelta) -> str:
        now = datetime.now(timezone.utc)

        return jwt.encode(
            {
                "user_id": user_id,
                "user_name": username,
                "exp": now + expires_at,
                "iat": now,
                "type": "access_token",
            },
            self.secret_key,
            self.encoding_algorithm
        )

    def decode_access_token(self, access_token: str) -> str:
        return jwt.decode(access_token, self.secret_key, self.encoding_algorithm)
