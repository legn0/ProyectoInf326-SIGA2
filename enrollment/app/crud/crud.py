from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.models import Enrollment_model, Parallel_data
from ..schemas.schemas import EnrollmentCreate, EnrollmentUpdate

class EnrollmentCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_enrollment(self, enrollment_id: int, course_id: int, parallel_id: int):
        return (
            self.db.query(Enrollment_model)
            .filter(
                Enrollment_model.id == enrollment_id,
                Enrollment_model.course_id == course_id,
                Enrollment_model.parallel_id == parallel_id,
                Enrollment_model.is_active == "Inscrita"
            )
            .first()
        )

    def list_enrollments(self, course_id: int, parallel_id: int):
        return (
            self.db.query(Enrollment_model)
            .filter(
                Enrollment_model.course_id == course_id,
                Enrollment_model.parallel_id == parallel_id,
                Enrollment_model.is_active == "Inscrita"
            )
            .all()
        )
    
    def get_enrollment_by_student_and_course(self, student_id: int, course_id: int, parallel_id: int):
        return self.db.query(Enrollment_model).filter(
            Enrollment_model.student_id == student_id,
            Enrollment_model.course_id == course_id,
            or_(
            Enrollment_model.is_active == "Inscrita",
            Enrollment_model.is_active == "Pendiente"
            )
        ).first()
    
    def get_pending_enrollments(self, course_id: int, parallel_id: int):
        return (
            self.db.query(Enrollment_model)
            .filter(
                Enrollment_model.course_id == course_id,
                Enrollment_model.parallel_id == parallel_id,
                Enrollment_model.is_active == "Pendiente" 
            )
            .all()
        )

    def create_enrollment(self, course_id: int, parallel_id: int, enrollment_data: EnrollmentCreate):
        new_enrollment = Enrollment_model(
            course_id = course_id,
            parallel_id = parallel_id,
            student_id = enrollment_data.student_id,
            is_active = "Pendiente"
        )
        self.db.add(new_enrollment)
        self.db.commit()
        self.db.refresh(new_enrollment)
        return new_enrollment

    def update_enrollment(self, enrollment_id: int, enrollment_data: EnrollmentUpdate):
        enrollment = (
            self.db.query(Enrollment_model)
            .filter(Enrollment_model.id == enrollment_id)
            .first()
        )
        if enrollment:
            enrollment.course_id = enrollment_data.course_id
            enrollment.parallel_id = enrollment_data.parallel_id
            enrollment.is_active = enrollment_data.is_active
            self.db.commit()
            self.db.refresh(enrollment)
            return enrollment
        return None

    def delete_enrollment(self, enrollment_id: int):
        enrollment = (
            self.db.query(Enrollment_model)
            .filter(Enrollment_model.id == enrollment_id)
            .first()
        )
        if enrollment:
            enrollment.is_active = "Eliminada"
            self.db.commit()
            return enrollment
        return None
    
    def get_course_and_parallel(self, course_id: int, parallel_id: int):
        return (
            self.db.query(Parallel_data)
            .filter(
                Parallel_data.course_id == course_id,
                Parallel_data.parallel_id == parallel_id,
                Parallel_data.is_deleted == False
            )
            .first()
        )
    
    def create_parallel(self, parallel_id: int, course_id: int):
        new_parallel = Parallel_data(
            course_id = course_id,
            parallel_id = parallel_id,
            is_deleted = False
        )
        self.db.add(new_parallel)
        self.db.commit()
        self.db.refresh(new_parallel)
        return new_parallel
    
    def delete_course(self, course_id):
        enrollments = (
            self.db.query(Enrollment_model)
            .filter(Enrollment_model.course_id == course_id)
        ).all()
        courses_deleted = (
            self.db.query(Parallel_data)
            .filter(Parallel_data.course_id == course_id)
        ).all()
        if enrollments:
            for enrollment in enrollments:
                enrollment.is_active = "Eliminada"
                self.db.commit()

        if courses_deleted:
            for courses in courses_deleted:
                courses.is_deleted = True
                self.db.commit()
        return None
    
    def delete_parallel(self, parallel_id):
        enrollments = (
            self.db.query(Enrollment_model)
            .filter(Enrollment_model.parallel_id == parallel_id)
        ).all()
        parallel_deleted = (
            self.db.query(Parallel_data)
            .filter(Parallel_data.parallel_id == parallel_id)
        ).all()
        
        if enrollments:
            for enrollment in enrollments:
                enrollment.is_active = "Eliminada"
                self.db.commit()
        if parallel_deleted:
            for parallel in parallel_deleted:
                parallel.is_deleted = True
                self.db.commit()
        return None