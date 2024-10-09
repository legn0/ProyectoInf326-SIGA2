from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    description: str
    sigla: str	
    departamento: str
    prerequisites: str
    

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True 