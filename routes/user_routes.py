from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.PaginatedResponseSchemas import PaginatedResponse
from schemas.UserSchemas import (
    UserCreate, RequestDetails, TokenSchema, UserOut, UserUpdate
)
from models.User import User
from database import get_db
from backend.utils import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

router = APIRouter()


# CREATE USER
@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(400, "Username already exists")

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already exists")

    new_user = User(
        username=payload.username,
        name = payload.name,
        password=get_hashed_password(payload.password),
        email=payload.email,
        department_name=payload.department_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# LOGIN
@router.post("/login", response_model=TokenSchema)
def login(request: RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(400, "Invalid username or password")

    if not verify_password(request.password, user.password):
        raise HTTPException(400, "Invalid username or password")

    access = create_access_token(user.id, "", user.username)
    refresh = create_refresh_token(user.id, user.username)

    return TokenSchema(
        access_token=access,
        refresh_token=refresh,
        username=user.username,
        email=user.email
    )



from pydantic import BaseModel
import os
import jwt

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    username: str
    email: str


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):

    try:
        secret = os.getenv("JWT_REFRESH_SECRET_KEY") or os.getenv("JWT_SECRET_KEY")
        algo = os.getenv("ALGORITHM", "HS256")

        data = jwt.decode(payload.refresh_token, secret, algorithms=[algo])
        user_id = data.get("sub")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(401, "User not found")

        new_access = create_access_token(user.id, "", user.username)

        return RefreshTokenResponse(
            access_token=new_access,
            username=user.username,
            email=user.email
        )

    except Exception:
        raise HTTPException(401, "Invalid refresh token")


@router.get("/", response_model=PaginatedResponse[UserOut])
def get_users(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))

    total = query.count()
    data = query.offset(skip).limit(limit).all()

    return PaginatedResponse(data=data, total=total)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user



@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if payload.username:
        existing_username = (
            db.query(User)
            .filter(User.username == payload.username, User.id != user_id)
            .first()
        )
        if existing_username:
            raise HTTPException(400, "Username already taken")

        user.username = payload.username

    if payload.email:
        existing_email = (
            db.query(User)
            .filter(User.email == payload.email, User.id != user_id)
            .first()
        )
        if existing_email:
            raise HTTPException(400, "Email already taken")

        user.email = payload.email

    if payload.department_name is not None:
        user.department_name = payload.department_name


    if payload.password:
        user.password = get_hashed_password(payload.password)

    db.commit()
    db.refresh(user)
    return user



@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")

    db.delete(user)
    db.commit()
