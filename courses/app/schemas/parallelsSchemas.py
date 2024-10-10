from pydantic import BaseModel

class ParallelBase(BaseModel):
    number: int
    limite_cupo: int
    jornada: int
    Campus: int

class ParallelCreate(ParallelBase):
    pass

# Agregar ParallelUpdate
class ParallelUpdate(BaseModel):
    name: str | None = None 
class Parallel(ParallelBase):
    id: int

    class Config:
        from_attributes = True