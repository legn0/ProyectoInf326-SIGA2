from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import get_db 
from ..models import coursesModel
from ..schemas import coursesSchemas 

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.get("/", response_model=list[coursesSchemas.Course])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(coursesModel.Course).all()
    return courses