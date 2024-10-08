from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database.db import Base

class Parallel(Base):
    __tablename__ = "parallels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="parallels") 