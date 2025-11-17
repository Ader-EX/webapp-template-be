from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from database import Base

class ConsultingManager(Base):
    __tablename__ = "consulting_managers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    department_name = Column(String(150), nullable=False)
    created_at = Column(DateTime, default =datetime.now(), nullable=True)
