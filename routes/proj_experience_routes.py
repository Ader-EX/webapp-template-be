from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PaginatedResponseSchemas
from models.ConsManager import ConsultingManager
from models.ProjExperience import ProjectExperience
from schemas.ProjManagerSchema import ProjectExperienceCreate, ProjectExperienceResponse, ProjectExperienceUpdate
from database import get_db


router = APIRouter()



@router.post("/", response_model=ProjectExperienceResponse)
def create_experience(
    data: ProjectExperienceCreate,
    db: Session = Depends(get_db), 
):
    new_project = ProjectExperience(
        **data.dict(),
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/", response_model=PaginatedResponseSchemas.PaginatedResponse[ProjectExperienceResponse])
def get_experiences(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProjectExperience)

    if search:
        query = query.filter(ProjectExperience.project_name.ilike(f"%{search}%"))

    total = query.count()
    data = query.offset(skip).limit(limit).all()

    return PaginatedResponseSchemas.PaginatedResponse(data=data, total=total)



@router.put("/{project_id}", response_model=ProjectExperienceResponse)
def update_project_experience(
    project_id: int,
    data: ProjectExperienceUpdate,
    db: Session = Depends(get_db)
):
    project = db.query(ProjectExperience).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(404, "Project experience not found")

    if data.consulting_manager_id:
        manager = db.query(ConsultingManager).filter_by(id=data.consulting_manager_id).first()
        if not manager:
            raise HTTPException(404, "Consulting manager does not exist")

        project.consulting_manager_id = data.consulting_manager_id

    db.commit()
    db.refresh(project)
    return project


# Delete project
@router.delete("/{project_id}")
def delete_experience(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(ProjectExperience).filter_by(id=project_id).first()
    if not proj:
        raise HTTPException(404, "Project experience not found")

    db.delete(proj)
    db.commit()
    return {"message": "Deleted successfully"}
