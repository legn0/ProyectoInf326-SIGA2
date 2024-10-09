from pydantic import BaseModel

class ParallelBase(BaseModel):
    name: str
    course_id: int
    number: int
    limite_cupo: int
    jornada: str
    Campus: str
    sala: str

class ParallelCreate(ParallelBase):
    pass

class Parallel(ParallelBase):
    id: int

    class Config:
        from_attributes = True