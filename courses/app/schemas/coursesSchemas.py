from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    sigla: str	
    creditos: int
    departamento: str
    prerequisites: str
    

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    name: str | None = None
    sigla: str    | None = None
    creditos: int | None = None
    departamento: str | None = None
    prerequisites: str | None = None

class Course(CourseBase):
    id: int
    prerequisites: str | None = None
    class Config:
        from_attributes = True 