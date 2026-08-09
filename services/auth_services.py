class AuthServices:

    def __init__(self):
        pass

    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass

    def get_password_hash(self, password: str) -> str:
        pass