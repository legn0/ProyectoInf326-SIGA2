
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import Classes
import uvicorn
import pytz

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules") ##Crear horario para un paralelo
def create_schedule(course_id: int, parallel_id: int, horario: Classes.HorarioParalelo):
    return "Horario creado con exito"

@app.put("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}") ##Actualizar informacion de un horario
def update_schedule(course_id: int, parallel_id: int, schedule_id: int):
    return 

@app.delete("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}") ##Eliminar horario
def delete_schedule(ccourse_id: int, parallel_id: int, schedule_id: int):
    return

@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}") ##Obtener informacion de un horario
def get_info_schedule(course_id: int, parallel_id: int, schedule_id: int):
    return

@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules") ##Listar todos los horarios de un paralelo
def get_parallel_schedule(course_id: int, parallel_id: int):
    return 