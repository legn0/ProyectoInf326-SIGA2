from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base 

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True) 
    description = Column(String(255))
    sigla = Column(String(255), unique=True, index=True)
    departamento = Column(String(255), unique=True, index=True)
    prerequisites = Column(String(255))
    # relationships
    parallels = relationship("Parallel", back_populates="course")