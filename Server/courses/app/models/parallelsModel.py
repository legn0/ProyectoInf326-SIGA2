from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from ..database.db import Base

class Parallel(Base):
    __tablename__ = "parallels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    number = Column(Integer)
    limite_cupo = Column(Integer)
    jornada = Column(SmallInteger)
    Campus = Column(SmallInteger)
    is_deleted = Column(Boolean, default=False)


    course = relationship("Course", back_populates="parallels") 
