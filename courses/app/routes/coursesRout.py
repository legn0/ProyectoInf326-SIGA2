from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import get_db 
from ..models import coursesModel
from ..schemas import coursesSchemas 

from ..rabbit.rabbitPublisher import get_rabbit_channel
from ..rabbit.parallelsRabbitFunctions import *

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.get("/", response_model=list[coursesSchemas.Course])
def get_courses(db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    courses = db.query(coursesModel.Course).all()
    publishUpdatedParallel(channel=channel, course_id=20, course_name="CC", parallel_id=10)
    return courses