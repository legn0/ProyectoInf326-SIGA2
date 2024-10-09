from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Crear una nueva inscripción
@app.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments", response_model=schemas.Enrollment)
def create_enrollment(course_id: int, parallel_id: int, enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.create_enrollment(db=db, enrollment=enrollment)

# Actualizar una inscripción existente
@app.put("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}", response_model=schemas.Enrollment)
def update_enrollment(course_id: int, parallel_id: int, enrollment_id: int, enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = crud.get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return crud.update_enrollment(db=db, enrollment_id=enrollment_id, enrollment=enrollment)

# Eliminar una inscripción
@app.delete("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}")
def delete_enrollment(course_id: int, parallel_id: int, enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = crud.get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return crud.delete_enrollment(db=db, enrollment_id=enrollment_id)

# Consultar una inscripción
@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}", response_model=schemas.Enrollment)
def read_enrollment(course_id: int, parallel_id: int, enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = crud.get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment

# Listar todas las inscripciones de un paralelo
@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments", response_model=list[schemas.Enrollment])
def list_enrollments(course_id: int, parallel_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_enrollments_by_parallel(db=db, parallel_id=parallel_id, skip=skip, limit=limit)