from datetime import timedelta
from http import HTTPStatus
from typing import  Annotated

from fastapi import FastAPI, APIRouter, Cookie, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select

from models import User, UserBase
from core import DatabaseManager, PasswordManager, TokenManager, configuration_manager
from dto import UserResponse, UserLoginRequest, UserSignupRequest, LogoutResponse, DeleteResponse
from utils.auth_utils import get_encoded_payload

auth_router = APIRouter()

token_manager: TokenManager = TokenManager(configuration_manager.secret_key, configuration_manager.encoding_algorithm)

@auth_router.post("/signup", status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def signup(
    user_request: UserSignupRequest,
    db: Session = Depends(DatabaseManager.get_session),
    auth_manager = Depends(PasswordManager)
) -> UserResponse:
    try:
        hashed_password: str = auth_manager.hash_password(user_request.password)
        user: User = User(name=user_request.name, email=UserBase.validate_email(user_request.email), hashed_password=hashed_password)

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserResponse(id = user.id, name = user.name, email = user.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/login", status_code=HTTPStatus.OK, response_model=UserResponse)
async def login(
    user_request: UserLoginRequest,
    response: Response,
    db: Session = Depends(DatabaseManager.get_session),
    auth_manager: PasswordManager = Depends(PasswordManager)
) -> UserResponse:
    try:
        sql_query = select(User).where(User.email == user_request.email)
        user = db.exec(sql_query).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found, Please check your email or sign up first")

        if not auth_manager.verify_password(user_request.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password, Please check your password and try again")

        access_token = token_manager.create_access_token(user_id=str(user.id),
                                                        email=user.email,
                                                        expires_at=timedelta(minutes=15))

        response.set_cookie(
            key="youtube_automation_access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )

        return UserResponse(id = user.id, name = user.name, email = user.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.delete("/logout", status_code=HTTPStatus.OK, response_model=LogoutResponse)
def logout(response: Response) -> LogoutResponse:
    response.delete_cookie(key="youtube_automation_access_token")

    return LogoutResponse(message="Successfully logged out")

@auth_router.delete("/delete", status_code=HTTPStatus.OK, response_model=DeleteResponse)
async def delete_user(
    request: Request,
    response: Response,
    db: Session = Depends(DatabaseManager.get_session),
) -> DeleteResponse:
    try:
        payload = get_encoded_payload(token_manager = token_manager, request = request, cookie_key = "youtube_automation_access_token", required_fields = ["user_id"])

        user = db.exec(
            select(User).where(User.id == payload["user_id"])
        ).first()

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found, Please check your sign up first",
            )

        db.delete(user)
        db.commit()

        return DeleteResponse(
            message="Account deleted successfully, All the data associated with the account has been removed",
            id=user.id,
            name=user.name,
            email=user.email,
        )
    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete account due to an internal server error",
        )
    finally:
        response.delete_cookie(
            key="youtube_automation_access_token",
            path="/",
        )

