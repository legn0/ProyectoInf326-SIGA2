from sqlalchemy.orm import Session
import models
import schemas

def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = models.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_enrollment(db: Session, enrollment_id: int):
    return db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()

def update_enrollment(db: Session, enrollment_id: int, enrollment: schemas.EnrollmentCreate):
    db_enrollment = get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment:
        db_enrollment.student_id = enrollment.student_id
        db_enrollment.parallel_id = enrollment.parallel_id
        db_enrollment.course_id = enrollment.course_id
        db.commit()
        db.refresh(db_enrollment)
    return db_enrollment

def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
    return db_enrollment

def get_enrollments_by_parallel(db: Session, parallel_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Enrollment).filter(models.Enrollment.parallel_id == parallel_id).offset(skip).limit(limit).all()