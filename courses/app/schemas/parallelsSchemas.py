from pydantic import BaseModel

class ParallelBase(BaseModel):
    name: str
    course_id: int

class ParallelCreate(ParallelBase):
    pass

class Parallel(ParallelBase):
    id: int

    class Config:
        from_attributes = True