from pydantic import BaseModel

class HorarioParalelo(BaseModel):
    siglacurso: str
    paralelo: int
    dia: str
    bloqueinicio: int
    bloquefinal: int


