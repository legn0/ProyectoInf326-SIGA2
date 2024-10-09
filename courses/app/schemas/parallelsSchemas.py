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

# Agregar ParallelUpdate
class ParallelUpdate(BaseModel):
    name: str | None = None 
class Parallel(ParallelBase):
    id: int

    class Config:
        from_attributes = True