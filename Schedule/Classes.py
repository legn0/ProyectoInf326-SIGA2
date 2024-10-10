from pydantic import BaseModel

class Horario(BaseModel):
    nombre_bloque: str | None = None
    id_bloque: int | None = None
    tipo_bloque: str | None = None

