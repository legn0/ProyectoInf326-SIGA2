from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.models import Enrollment_model
from ..schemas.schemas import Enrollment, EnrollmentCreate, EnrollmentUpdate

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
            Enrollment_model.parallel_id == parallel_id,
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
                Enrollment_model.is_active == "Pendiente"  # Verifica el estado "Pendiente"
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