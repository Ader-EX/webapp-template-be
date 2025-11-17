from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.PaginatedResponseSchemas import PaginatedResponse
from models.ConsManager import ConsultingManager
from schemas.ConsManagerSchema import ConsultingManagerCreate, ConsultingManagerResponse
from database import get_db

from dependencies import verify_access_token

router = APIRouter()


@router.post("/", response_model=ConsultingManagerResponse)
def create_manager(data: ConsultingManagerCreate, db: Session = Depends(get_db)):
    new_manager = ConsultingManager(**data.dict())
    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)
    return new_manager


@router.get("/", response_model=PaginatedResponse[ConsultingManagerResponse])
def get_managers(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ConsultingManager)

    if search:
        query = query.filter(ConsultingManager.name.ilike(f"%{search}%"))

    total = query.count()
    data = query.offset(skip).limit(limit).all()

    return PaginatedResponse(data=data, total=total)



@router.get("/{manager_id}", response_model=ConsultingManagerResponse)
def get_manager(manager_id: int, db: Session = Depends(get_db)):
    manager = db.query(ConsultingManager).filter_by(id=manager_id).first()
    if not manager:
        raise HTTPException(404, "Consulting Manager not found")
    return manager


@router.delete("/{manager_id}")
def delete_manager(manager_id: int, db: Session = Depends(get_db)):
    manager = db.query(ConsultingManager).filter_by(id=manager_id).first()
    if not manager:
        raise HTTPException(404, "Consulting Manager not found")

    db.delete(manager)
    db.commit()
    return {"message": "Deleted successfully"}
