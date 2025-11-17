from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# CREATE
class UserCreate(BaseModel):
    username: str
    name: str
    password: str
    email: str
    department_name: Optional[str] = None


# LOGIN
class RequestDetails(BaseModel):
    username: str
    password: str


# TOKEN RESPONSE
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    username: str
    email: str


# OUTPUT
class UserOut(BaseModel):
    id: int
    username: str
    name: str
    
    email: str
    department_name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    department_name: Optional[str] = None
