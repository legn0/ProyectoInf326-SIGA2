from sqlalchemy.orm import Session
import models
import schemas

def create_enrollment(db: Session, enrollment_data: dict):
    new_enrollment = models.Enrollment(**enrollment_data)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

def get_enrollment(db: Session, enrollment_id: int):
    return db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()

def get_enrollments_by_parallel(db: Session, parallel_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Enrollment).filter(models.Enrollment.parallel_id == parallel_id).offset(skip).limit(limit).all()

def update_enrollment(db: Session, enrollment_data: dict):
    db_enrollment = get_enrollment(db, enrollment_id=enrollment_data["id"])
    if db_enrollment:
        db_enrollment.parallel_id = enrollment_data["parallel_id"]
        db_enrollment.course_id = enrollment_data["course_id"]
        db.commit()
        db.refresh(db_enrollment)
    return db_enrollment 

def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
    return db_enrollment