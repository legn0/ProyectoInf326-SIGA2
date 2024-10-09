from pydantic import BaseModel

class EnrollmentBase(BaseModel):
    student_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int

    class Config:
        orm_mode = True