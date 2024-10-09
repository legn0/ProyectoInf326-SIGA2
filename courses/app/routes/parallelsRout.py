from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.db import get_db
from ..models import parallelsModel, coursesModel
from ..schemas import parallelsSchemas

router = APIRouter(
    prefix="/courses/{course_id}/parallels",
    tags=["Parallels"]
)

# Crear un paralelo
@router.post("/", response_model=parallelsSchemas.Parallel, status_code=status.HTTP_201_CREATED)
def create_parallel(course_id: int, parallel: parallelsSchemas.ParallelCreate, db: Session = Depends(get_db)):
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_parallel = parallelsModel.Parallel(**parallel.dict(), course_id=course_id)
    db.add(db_parallel)
    db.commit()
    db.refresh(db_parallel)
    return db_parallel

# Actualizar un paralelo
@router.put("/{parallel_id}", response_model=parallelsSchemas.Parallel)
def update_parallel(course_id: int, parallel_id: int, parallel: parallelsSchemas.ParallelUpdate, db: Session = Depends(get_db)):
    db_parallel = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.id == parallel_id, parallelsModel.Parallel.course_id == course_id).first()
    if not db_parallel:
        raise HTTPException(status_code=404, detail="Parallel not found")

    for key, value in parallel.dict(exclude_unset=True).items():
        setattr(db_parallel, key, value)

    db.commit()
    db.refresh(db_parallel)
    return db_parallel

# Eliminar un paralelo
@router.delete("/{parallel_id}")
def delete_parallel(course_id: int, parallel_id: int, db: Session = Depends(get_db)):
    db_parallel = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.id == parallel_id, parallelsModel.Parallel.course_id == course_id).first()
    if not db_parallel:
        raise HTTPException(status_code=404, detail="Parallel not found")

    db.delete(db_parallel)
    db.commit()
    return {"message": "Parallel deleted successfully"}

# Consultar un paralelo
@router.get("/{parallel_id}", response_model=parallelsSchemas.Parallel)
def get_parallel(course_id: int, parallel_id: int, db: Session = Depends(get_db)):
    db_parallel = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.id == parallel_id, parallelsModel.Parallel.course_id == course_id).first()
    if not db_parallel:
        raise HTTPException(status_code=404, detail="Parallel not found")

    return db_parallel

# Listar todos los paralelos de un curso
@router.get("/", response_model=List[parallelsSchemas.Parallel])
def get_parallels(course_id: int, db: Session = Depends(get_db)):
    db_parallels = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.course_id == course_id).all()
    return db_parallels