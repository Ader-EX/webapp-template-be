import os
from datetime import datetime, timedelta
from typing import Union, Any, Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


# Password hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 token dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


# -------------------------
# Password Utilities
# -------------------------

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


# -------------------------
# User + Token Handling
# -------------------------

def get_current_user_name(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extract username ("un") from JWT token.
    """
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )

        username: str = payload.get("un")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Invalid token"
            )

        return username

    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid or expired token"
        )


def create_access_token(
    subject: Union[str, Any],
    role: str,
    name: str,
    expires_delta: int = None
) -> str:

    if expires_delta is not None:
        exp = datetime.now() + expires_delta
    else:
        exp = datetime.now() + timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 600))
        )

    payload = {
        "sub": str(subject),
        "un": name,
        "rl": role,
        "exp": exp
    }

    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY"),
        os.getenv("ALGORITHM")
    )


def create_refresh_token(
    subject: Union[str, Any],
    name: str,
    expires_delta: int = None
) -> str:

    if expires_delta is not None:
        exp = datetime.now() + expires_delta
    else:
        exp = datetime.now() + timedelta(minutes=600)

    payload = {
        "sub": str(subject),
        "un": name,
        "exp": exp
    }

    return jwt.encode(
        payload,
        os.getenv("JWT_REFRESH_SECRET_KEY"),
        os.getenv("ALGORITHM")
    )
