from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ProjectExperience(Base):
    __tablename__ = "project_experience"

    id = Column(Integer, primary_key=True, index=True)

    no_sales_order = Column(String(200), nullable=False)
    customer_name = Column(String(200), nullable=False)
    project_name = Column(String(200), nullable=False)
    project_year = Column(String(4), nullable=False)
    category = Column(String(150), nullable=False)
    created_at = Column(DateTime, default =datetime.now(), nullable=True)

    consulting_manager_id = Column(
        Integer,
        ForeignKey("consulting_managers.id"),
        nullable=True
    )

    
    consulting_manager = relationship("ConsultingManager")
