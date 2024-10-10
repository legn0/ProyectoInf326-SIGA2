from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import get_db 

from ..models import coursesModel
from ..schemas import coursesSchemas 

from ..rabbit.rabbitPublisher import get_rabbit_channel

from pika.adapters.blocking_connection import BlockingChannel

from ..rabbit.courseRabbitFunctions import *

router = APIRouter(
    prefix="/api/v1/courses",
    responses={404: {"description": "Not found"}},
    tags=["Courses"]
)

@router.get("/", response_model=list[coursesSchemas.Course])
def get_courses(db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    courses = db.query(coursesModel.Course).all()
    return courses

@router.get("/{id}", response_model=coursesSchemas.Course) #course por id
def get_course(id: int, db: Session = Depends(get_db)):

    course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=coursesSchemas.Course) #Crear course
def create_course(course: coursesSchemas.CourseCreate, db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    db_course = coursesModel.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    publishCreateCourse(course_id = db_course.id,
                        course_name=db_course.name,
                        sigla= db_course.sigla,
                        creditos=db_course.creditos,
                        departamento=db_course.departamento,
                        prerequisitos=db_course.prerequisites,
                        channel=channel)
    return db_course

@router.put("/{id}", response_model=coursesSchemas.Course) #Actualizar course
def update_course(id: int, course: coursesSchemas.CourseUpdate, db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id)
    if not db_course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db_course.update(course.dict(), synchronize_session=False)
    db.commit()
    publishUpdatedCourse(channel=channel,
                         course_id=db_course.first().id,
                         **course.dict(exclude_unset=True))
    return db_course.first()

@router.delete("/{id}", response_model=coursesSchemas.Course) #Eliminar course
def delete_course(id: int, db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id)
    if not db_course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    publishDeletedCourse(channel=channel,
                         course_id=db_course.first().id)
    db_course.delete()
    db.commit()
    
    return db_course.first()
