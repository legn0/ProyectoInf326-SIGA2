from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import get_db 

from ..models import coursesModel
from ..schemas import coursesSchemas
from ..models import parallelsModel
from ..schemas import parallelsSchemas 

router = APIRouter(
    prefix="/api/v1/courses",
    responses={404: {"description": "Not found"}},
    tags=["Courses"]
)

@router.get("/", response_model=list[coursesSchemas.Course]) #Lista de courses
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(coursesModel.Course).all()
    return courses

@router.get("/{id}", response_model=coursesSchemas.Course) #course por id
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=coursesSchemas.Course) #Crear course
def create_course(course: coursesSchemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = coursesModel.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/{id}", response_model=coursesSchemas.Course) #Actualizar course
def update_course(id: int, course: coursesSchemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id)
    if not db_course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db_course.update(course.dict(), synchronize_session=False)
    db.commit()
    return db_course.first()

@router.delete("/{id}", response_model=coursesSchemas.Course) #Eliminar course
def delete_course(id: int, db: Session = Depends(get_db)):
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id)
    if not db_course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db_course.delete()
    db.commit()
    return db_course.first()

@router.get("/{id}/parallels", response_model=list[parallelsSchemas.Parallel]) #Lista de parallels por course
def get_parallels(id: int, db: Session = Depends(get_db)):
    parallels = db.query(coursesModel.Parallel).filter(coursesModel.Parallel.course_id == id).all()
    return parallels
    

@router.post("/{id}/parallels", response_model=parallelsSchemas.Parallel) #Crear parallel por course
def create_parallel(id: int, parallel: parallelsSchemas.ParallelCreate, db: Session = Depends(get_db)):
    db_parallel = coursesModel.Parallel(**parallel.dict(), course_id=id)
    db.add(db_parallel)
    db.commit()
    db.refresh(db_parallel)
    return db_parallel

@router.put("/{id}/parallels/{parallel_id}", response_model=parallelsSchemas.Parallel) #Actualizar parallel por course
def update_parallel(id: int, parallel_id: int, parallel: parallelsSchemas.ParallelCreate, db: Session = Depends(get_db)):
    db_parallel = db.query(parallelsSchemas.Parallel).filter(parallelsSchemas.Parallel.id == parallel_id)
    if not db_parallel.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parallel not found")
    db_parallel.update(parallel.dict(), synchronize_session=False)
    db.commit()
    return db_parallel.first()

@router.delete("/{id}/parallels/{parallel_id}", response_model=parallelsSchemas.Parallel) #Eliminar parallel por course
def delete_parallel(id: int, parallel_id: int, db: Session = Depends(get_db)):
    db_parallel = db.query(parallelsSchemas.Parallel).filter(parallelsSchemas.Parallel.id == parallel_id)
    if not db_parallel.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parallel not found")
    db_parallel.delete()
    db.commit()
    return db_parallel.first()

@router.get("/{id}/parallels/{parallel_id}", response_model=parallelsSchemas.Parallel) #Consultar paralelo por course
def get_parallel(id: int, parallel_id: int, db: Session = Depends(get_db)):
    parallel = db.query(parallelsSchemas.Parallel).filter(parallelsSchemas.Parallel.id == parallel_id).first()
    if not parallel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parallel not found")
    return parallel