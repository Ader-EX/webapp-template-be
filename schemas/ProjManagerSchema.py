from pydantic import BaseModel
from typing import Optional

class ProjectExperienceBase(BaseModel):
    no_sales_order: str
    customer_name: str
    project_name: str
    project_year: str
    consulting_manager_id:int
    category: str


class ProjectExperienceCreate(ProjectExperienceBase):
    pass


class ProjectExperienceUpdate(BaseModel):
    consulting_manager_id: Optional[int] = None


class ProjectExperienceResponse(ProjectExperienceBase):
    id: int
    consulting_manager_id: Optional[int]
    class Config:
        orm_mode = True
