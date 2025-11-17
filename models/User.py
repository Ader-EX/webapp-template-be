from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from database import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username= Column(String(50), nullable=False, unique=True)
    name= Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email= Column(String(50), nullable=False, unique=True)
    department_name= Column(String(255))
    created_at = Column(DateTime, default =datetime.now(), nullable=True)
