from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base 

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    sigla = Column(String(255), unique=True, index=True)
    departamento = Column(String(255), index=True)
    prerequisites = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False)
    # relationships
    parallels = relationship("Parallel", back_populates="course")