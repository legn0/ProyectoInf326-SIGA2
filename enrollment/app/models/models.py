from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from ..database.database import Base

class Enrollment_model(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    parallel_id = Column(Integer, index=True)
    course_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(String(20), default="Pendiente")  # Valores: "Inscrita", "Pendiente", "Eliminada"