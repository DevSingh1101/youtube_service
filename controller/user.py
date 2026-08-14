from datetime import timedelta
from http import HTTPStatus
from typing import Dict, Annotated

from fastapi import FastAPI, APIRouter, Cookie, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select

from models import User
from core import DatabaseManager, PasswordManager, TokenManager, configuration_manager
from dto import UserResponse, UserSignupRequest, LogoutResponse, DeleteResponse

user_router = APIRouter(prefix="/user", tags=["user"])

token_manager: TokenManager = TokenManager(configuration_manager.secret_key, configuration_manager.encoding_algorithm)

@user_router.post("/auth/signup", status_code=HTTPStatus.CREATED)
async def signup(
    user: UserSignupRequest,
    db: Session = Depends(DatabaseManager.get_session),
    auth_manager = Depends(PasswordManager)
) -> UserResponse:
    try:
        hashed_password: str = auth_manager.hash_password(user.password)
        new_user: User = User(name=user.name, username=user.username, hashed_password=hashed_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserResponse(id = new_user.id, name = new_user.name, username = new_user.username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/auth/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(DatabaseManager.get_session),
    auth_manager: PasswordManager = Depends(PasswordManager)
) -> UserResponse:
    try:
        sql_query = select(User).where(User.username == form_data.username)
        user = db.exec(sql_query).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found, Please check your username or sign up first")

        if not auth_manager.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password, Please check your password and try again")

        access_token = token_manager.create_access_token(user_id=str(user.id),
                                                        username=user.username,
                                                        expires_at=timedelta(minutes=15))

        response.set_cookie(
            key="youtube_automation_access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )

        return UserResponse(id = user.id, name = user.name, username = user.username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.delete("/auth/logout")
def logout(response: Response) -> LogoutResponse:
    response.delete_cookie(key="youtube_automation_access_token")

    return LogoutResponse(message="Successfully logged out")

@user_router.delete("/auth/delete", response_model=DeleteResponse)
async def delete_user(
    request: Request,
    response: Response,
    db: Session = Depends(DatabaseManager.get_session),
) -> DeleteResponse:
    access_token: str | None = request.cookies.get("youtube_automation_access_token")

    if not access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Login required to delete account",
        )

    try:
        payload = token_manager.decode_access_token(access_token)

        if not payload or not payload.get("user_id"):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid or expired access token",
            )

        user_id = payload["user_id"]

        user = db.exec(
            select(User).where(User.id == user_id)
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
            username=user.username,
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
