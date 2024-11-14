from pydantic import BaseModel
from typing import Optional

# Modelo para crear o actualizar horario en la tabla horarios
class Horario(BaseModel):
    id_bloque: Optional[int] = None
    nombre_bloque: Optional[str] = None  # Nombre del bloque, e.g., "1-2"
    tipo: Optional[str] = None            # Tipo de horario, e.g., "Clase", "Ayudantia", "Laboratorio"
    id_profesor: Optional[int] = None
    nombre_profesor: Optional[str] = None
    dia: Optional[str] = None            # Dia de la semana, e.g., "Lunes", "Martes", "Miercoles", "Jueves", "Viernes"

    class Config:
        orm_mode = True

