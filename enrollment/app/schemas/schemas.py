from pydantic import BaseModel
from datetime import datetime

class Enrollment(BaseModel):
    id: int
    student_id: int
    course_id: int 
    parallel_id: int 
    created_at: datetime 
    is_active: str

    class Config:
        orm_mode = True
    
class EnrollmentCreate(BaseModel):
    student_id: int
    
    class Config:
        orm_mode = True

class EnrollmentUpdate(BaseModel):
    course_id: int 
    parallel_id: int
    is_active: str
    
    class Config:
        orm_mode = True