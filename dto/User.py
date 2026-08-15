from pydantic import BaseModel

class MessageResponse(BaseModel):
    message: str

class ChannelResponse(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserSignupRequest(BaseModel):
    name: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class LogoutResponse(MessageResponse):
    pass

class DeleteResponse(MessageResponse, UserResponse):
    pass