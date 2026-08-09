from pydantic import BaseModel


class ChannelResponse(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    username: str

class UserSignupRequest(BaseModel):
    name: str
    username: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str