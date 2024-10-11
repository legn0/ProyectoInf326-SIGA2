from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    parallel_id = Column(Integer, index=True)
    course_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)